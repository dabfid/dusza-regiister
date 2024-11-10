from flask import Blueprint, render_template, flash, g
from flask import redirect, url_for

from app.tables import Teams, Deadline, Notifications  # pyright: ignore
from app.tables import db  # pyright: ignore
from app.tables import Perms

from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user,
)

from app.forms import RegisterForm, UpdateForm, LoginForm, ChangePasswordForm  # pyright: ignore
from app import app  # pyright: ignore

from datetime import datetime

from pymysql import IntegrityError

students = Blueprint(
    "students_bp", __name__, static_folder="static", template_folder="templates"
)

"""
A jelentkező diákokhoz tartozó route-okat tartalmazó blueprint.
"""
login_student = LoginManager()
login_student.init_app(app)
login_student.login_view = "students_bp.login"


@login_student.user_loader
def load_user(user_id):
    return Teams.query.get_or_404(user_id)

@students.before_request
def load_user_info():
    g.perms = 1
    g.team_id = current_user.id
    g.notifications = Notifications.query.all()

@students.route("/", methods=["GET"])
def index():
    flash('halieeizu occse')
    return render_template("base.html")

@students.route("/register", methods=["GET", "POST"])
def register():
    g.perms = 0

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data

        school = form.school.data

        t1 = form.teammate1.data
        t2 = form.teammate2.data
        t3 = form.teammate3.data

        g1 = form.grade1.data
        g2 = form.grade2.data
        g3 = form.grade3.data

        if form.extra_teammate.data:
            t_extra = form.extra_teammate.data
        else:
            t_extra = None

        if form.extra_grade:
            g_extra = form.extra_grade.data
        else:
            g_extra = None

        teachers = form.teachers.data

        category = form.category.data
        language = form.language.data

        if confirm_password != password:
            flash("A két jelszó nem egyezik!")
            return render_template(
                "register.html",
                form=form)

        new_team = Teams()
        new_team.username = username
        new_team.password = password
        new_team.email = email
        new_team.school_id = school
        new_team.teammate1 = t1
        new_team.teammate2 = t2
        new_team.teammate3 = t3
        new_team.grade1 = g1
        new_team.grade2 = g2
        new_team.grade3 = g3
        new_team.teammate_extra = t_extra
        new_team.grade_extra = g_extra
        new_team.teachers = teachers
        new_team.category = category
        new_team.language = language
        try:
            db.session.add(new_team)
            db.session.commit()
            flash("Sikeres regisztráció!")
        except IntegrityError:
            db.session.rollback()
            flash("A felhasználónév vagy email cim már foglalt!")
        return render_template('students_bp.index')
    return render_template(
        "register.html",
        form=form)


@students.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    form = UpdateForm()
    team = Teams.query.get_or_404(id)

    if form.validate_on_submit():
        team.team_name = form.team_name.data
        team.school_id = form.school.data
        team.teammate1 = form.teammate1.data
        team.teammate2 = form.teammate2.data
        team.teammate3 = form.teammate3.data
        team.grade1 = form.grade1.data
        team.grade2 = form.grade2.data
        team.grade3 = form.grade3.data
        team.teammate_extra = form.extra_teammate.data
        team.grade_extra = form.extra_grade.data
        team.teachers = form.teachers.data
        team.category = form.category.data
        team.language = form.language.data
        try:
            db.session.commit()
            flash("Verseny adatok sikeresen frissítve!")
            return render_template("edit.html", form=form, team=team)
        except:
            flash("Hiba történt a frissítés során!")
            return render_template("edit.html", form=form, team=team)
    return render_template("edit.html", form=form, team=team)


@students.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Teams.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Helytelen jelszó vagy felhasználónév")
            return render_template("login.html", form=form)

        if user.check_password_hash(password):
            login_user(user)
        else:
            flash("Helytelen jelszó vagy felhasználónév")
    return render_template("students.login.html", form=form)

@students.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = Teams.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        old_password = form.old_password.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if not user.check_password_hash(old_password):
            flash("Helytelen jelszó")
            return render_template("change_password.html", form=form)

        if password != confirm_password:
            flash("A megadott jelszavak nem egyeznek")
            return render_template("change_password.html", form=form)
        
        user.password = password
        db.session.commit()
        flash("Sikeres jelszóváltoztatás")

    return redirect(url_for("dashboard_bp.index"))


@students.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard_bp.login"))
