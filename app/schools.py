from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user

from app.tables import Schools, Teams
from app.tables import db

from app.forms import LoginForm, UpdateSchoolForm, ValidateTeamForm

schools = Blueprint("schools_bp", __name__, static_folder="static", template_folder="templates")

@schools.route('/teams', methods=['GET'])
def teams():
    return render_template("teams.html", 
                           teams=Schools.query.all())

@schools.route('/teams/<int:id>', methods=['GET', 'POST'])
def view_and_validate_team(id):
    team = Schools.query.get_or_404(id)
    form = ValidateTeamForm()

    if form.validate_on_submit():
        team.is_valid = form.is_valid.data
        db.session.commit()
        flash("A csapat adatai sikeresen jóváhagyva!", "success")

    return render_template("view_team.html", 
                           team=Schools.query.get_or_404(id),
                           form=form,
                           validated=team.is_valid)

@schools.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = UpdateSchoolForm()
    school = Schools.query.get_or_404(id)
    if form.validate_on_submit():
        school.contact_name = form.contact_name.data
        school.contact_email = form.contact_email.data
        school.school_name = form.school_name.data
        db.session.commit()

        flash("School updated successfully", "success")
    return render_template("edit_school.html", 
                           form=form, 
                           school=school)

@schools.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Schools.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        if user.check_password(password):
            login_user(user)
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@schools.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard_bp.login"))

