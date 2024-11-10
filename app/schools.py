from flask import Blueprint, render_template, request, redirect, url_for, flash, g

from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user, current_user

from app.tables import Schools, Teams, Notifications
from app.tables import db
from app.tables import Status, Perms

from app.forms import LoginForm, UpdateSchoolForm, ValidateTeamForm, ChangePasswordForm

schools = Blueprint(
    "schools_bp", __name__, static_folder="static", template_folder="templates"
)


@schools.before_request
def load_user_info():
    g.perms = 3

@schools.route("/teams", methods=["GET"])
def teams():
    teams = Schools.query.filter_by(school_id=current_user.id).all()
    return render_template("teams.html", teams=teams)


@schools.route("/teams/<int:id>", methods=["GET", "POST"])
def team(id):
    team = Schools.query.get_or_404(id)
    return render_template("view_team.html", team=team)


# csapatok adatainak jováhagyása
@schools.route("/validate_team/<int:team_id>", methods=["POST"])
@login_required
def validate_team(team_id):
    previous = request.referrer

    team = Teams.query.get_or_404(team_id)
    team.status = Status.VALIDATED_BY_ADMIN
    db.session.commit()

    return redirect(previous)


@schools.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = UpdateSchoolForm()
    school = Schools.query.get_or_404(id)
    if form.validate_on_submit():
        school.contact_name = form.contact_name.data
        school.contact_email = form.contact_email.data
        school.school_name = form.school_name.data
        db.session.commit()

        flash("Az iskola adatai sikeresen frissültek")
    return render_template("edit_school.html", form=form, school=school)


@schools.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Schools.query.filter_by(username=username).first()

        if not user or not user.check_password_hash(password):
            flash("Helytelen jelszó vagy felhasználónév")
            return render_template("login.html", form=form)

        if user.check_password(password):
            login_user(user)
        else:
            flash("Helytelen jelszó vagy felhasználónév")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


@schools.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard_bp.login"))


@schools.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = Schools.query.get_or_404(current_user.id)
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
