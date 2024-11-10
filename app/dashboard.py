from flask import (
    Blueprint,
    render_template,
    request,
    session,
    abort,
    url_for,
    redirect,
    flash,
    g,
)

from flask_login import LoginManager, current_user
from flask_login import login_required, login_user, logout_user

from app.forms import AddLanguageForm, AddCategoryForm

from app.tables import (
    Languages,
    Admins,
    Teams,
    Categories,
    Notifications,
    Schools,
    Deadline,
    RegisterNewAdminForm,
    ChangePasswordForm,
    db,
)  # pyright: ignore
from app.tables import Status, Perms

from app.forms import LoginForm, ValidateTeamForm, AddSchoolForm, ModifyDeadlineForm  # pyright: ignore

from app import app  # pyright: ignore

import plotly
import plotly.express as px
import json
import pandas

from datetime import datetime

dashboard = Blueprint(
    "dashboard_bp", __name__, static_folder="static", template_folder="templates"
)

# Login manager handler
login_admin = LoginManager()
login_admin.init_app(app)
login_admin.login_view = "dashboard_bp.login"


@login_admin.user_loader
def load_user(user_id):
    return Admins.query.get_or_404(user_id)


@dashboard.before_request
def load_user_info():
    if hasattr(current_user, "username"):
        if current_user.username:
            g.user = current_user
            g.perms = Perms.STUDENT
        else:
            g.user = None
            g.perms = None


# dashboard főoldal
@dashboard.route("/", methods=["GET"])
@login_required
def index():
    return render_template("dashboard.html")


# bejelentkezés
@dashboard.route("/login", methods=["GET", "POST"])
def login():
    next = request.args.get("next")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Admins.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Helytelen felhasználónév vagy jelszó")
            return render_template("login.html", form=form)

        if user.check_password(password):
            login_user(user)
            return redirect(next or url_for("dashboard_bp.index"))
        else:
            flash("Helytelen felhasználónév vagy jelszó")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


# kijelentkezés
@dashboard.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard_bp.login"))


# programozási nyelvek megjelenitése, kezelése
@dashboard.route("/languages", methods=["GET", "POST"])
@login_required
def languages():
    form = AddLanguageForm()
    language = None
    result = Languages.query.all

    if form.validate_on_submit():
        language = form.language.data
        new_language = Languages(name=language)
        db.session.add(new_language)
        db.session.commit()
        form.language.data = ""

    return render_template("languages.html", language=language, form=form, list=result)


# versenykategoriák megjelenitése, kezelése
@dashboard.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    form = AddCategoryForm()
    category = None
    result = Categories.query.all()

    if form.validate_on_submit():
        category = form.categorie.data
        new_category = Categories(name=category)
        db.session.add(new_category)
        db.session.commit()
        form.category.data = ""

    return render_template("categories.html", category=category, form=form, list=result)


# programozási nyelv törlése az adatbázisból
@dashboard.route("/delete_language/<int:item_id>", methods=["POST"])
@login_required
def delete_language(lang_id):
    language = Languages.query.get(lang_id)
    is_used = Teams.query.filter_by(language=lang_id).count() > 0

    if is_used:
        flash("Ez a nyelv használatban van egy csapat által.")
        return render_template(
            "languages.html",
            language=language,
            form=AddLanguageForm(),
            list=Languages.query.all(),
        )
    if language:
        db.session.delete(language)
        db.session.commit()
    return render_template(
        "languages.html",
        language=language,
        form=AddLanguageForm(),
        list=Languages.query.all(),
    )


# versenykategoria törlése az adatbázisból
@dashboard.route("/delete_category/<int:item_id>", methods=["POST"])
@login_required
def delete_category(category_id):
    category = Categories.query.get(category_id)
    is_used = Teams.query.filter_by(category=category_id).count() > 0

    if is_used:
        flash("Ez a kategória használatban van egy csapat által")
        return render_template(
            "categories.html",
            category=category,
            form=AddCategoryForm(),
            list=Categories.query.all(),
        )

    if category:
        db.session.delete(category)
        db.session.commit()
    return render_template(
        "categories.html",
        category=category,
        form=AddCategoryForm(),
        list=Categories.query.all(),
    )


# csapatok megjelenitése
@dashboard.route("/teams", methods=["GET"])
def teams():
    teams = Teams.query.all()
    
    return render_template("teams.html", teams=teams)


# egyes csapatok megjelenitése, kezelése
@dashboard.route("/team/<int:team_id>", methods=["GET"])
@login_required
def team(team_id):
    team = Teams.query.get_or_404(team_id)
    return render_template("view_team.html", team=team)


@dashboard.route("/notify/<int:team_id>", methods=["POST"])
@login_required
def notify(team_id):
    previous = request.referrer

    new_notification = Notifications(
        message="Hiánypótlás", team_id=team_id, date=datetime.now()
    )
    db.session.add(new_notification)
    db.session.commit()

    return redirect(previous)


# csapatok adatainak jováhagyása
@dashboard.route("/validate_team/<int:team_id>", methods=["GET"])
@login_required
def validate_team(team_id):
    previous = request.referrer

    team = Teams.query.get_or_404(team_id)
    team.status = Status.VALIDATED_BY_ADMIN
    db.session.commit()

    return redirect(previous)


# iskolák adatainak megjelenitése
@dashboard.route("/schools", methods=["GET"])
@login_required
def schools():
    schools = Schools.query.all()
    return render_template("schools.html", schools=schools)


# új iskola hozzáadása
@dashboard.route("/schools/add_school", methods=["GET", "POST"])
@login_required
def add_school():
    form = AddSchoolForm()
    username = None
    password = None
    confirm_password = None

    contact_name = None
    contact_email = None

    school_name = None
    school_address = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        contact_name = form.contact_name.data
        contact_email = form.contact_email.data

        school_name = form.school_name.data
        school_address = form.school_address.data

        if password != confirm_password:
            flash("A megadott jelszavak nem egyeznek")
            return render_template("add_school.html", form=form)

        new_school = Schools(
            username=username,
            password=password,
            contact_name=contact_name,
            contact_email=contact_email,
            school_name=school_name,
            school_address=school_address,
        )
        db.session.add(new_school)
        db.session.commit()
        return redirect(url_for("dashboard_bp.schools"))
    return render_template("add_school.html", form=form)


@dashboard.route("/schools/delete/<int:id>", methods=["POST"])
@login_required
def delete_school(id):
    previous = request.referrer

    school = Schools.query.get_or_404(id)
    db.session.delete(school)
    db.session.commit()

    redirect(previous)


# csapatok adatai letöltése csv formátumban
@dashboard.route("/download/<int:id>", methods=["GET"])
@login_required
def download(id):
    team = Teams.query.get_or_404(id)
    output = (
        f"{team.email},"
        + f"{team.team_name},"
        + f"{team.teammate1},"
        + f"{team.teammate2},"
        + f"{team.teammate3},"
        + f"{team.grade1},"
        + f"{team.grade2},"
        + f"{team.grade3},"
        + f"{team.teammate_extra},"
        + f"{team.grade_extra},"
        + f"{team.teachers},"
        + f"{team.category},"
        + f"{team.language},"
        + f"{team.school_id},"
        + f"{team.status},"
    )

    return (
        output,
        200,
        {
            "Content-Type": "text/csv",
            "Content-Disposition": f"attachment; filename={id}.csv",
        },
    )


# határidő modosítása
@dashboard.route("/deadline", methods=["GET", "POST"])
@login_required
def deadline():
    form = ModifyDeadlineForm()
    deadline = Deadline.query.first()
    if form.validate_on_submit():
        deadline.date = form.deadline
        db.session.commit()
    return render_template("deadline.html", form=form, deadline=deadline)

@dashboard.route("/new_admin", methods=["GET"])
def new_admin():
    form = RegisterNewAdminForm()
    username = None
    password = None
    confirm_password = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if password != confirm_password:
            flash("A megadott jelszavak nem egyeznek")
            return render_template("new_admin.html", form=form)

        new_admin = Admins(username=username)
        new_admin.password(password)
        db.session.add(new_admin)
        db.session.commit()
        flash("Sikeres regisztráció")
    return render_template("new_admin.html",
                           form=form)

@dashboard.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    user = Admins.query.get_or_404(current_user.id)
    if form.validate_on_submit():
        old_password = form.old_password.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        
        if not user.check_password(old_password):
            flash("Helytelen jelszó")
            return render_template("change_password.html", form=form)

        if password != confirm_password:
            flash("A megadott jelszavak nem egyeznek")
            return render_template("change_password.html", form=form)
        
        user.password(password)
        db.session.commit()
        flash("Sikeres jelszóváltoztatás")

    return redirect(url_for("dashboard_bp.index"))

# statisztikák megjelenitése részletesebben
@dashboard.route("/statistics", methods=["GET"])
@login_required
def statistics():
    return render_template("statistics.html", graphJSON=language_count())


# Gráf készítése a csapatok számáról
def team_count():
    teams = Teams.query.with_entities(
        Teams.grade1, Teams.grade2, Teams.grade3, Teams.grade_extra
    ).all()
    grade_count = [0, 0, 0, 0, 0]
    for team in teams:
        for grade in team:
            if grade == 9:
                grade_count[0] += 1
            if grade == 10:
                grade_count[1] += 1
            if grade == 11:
                grade_count[2] += 1
            if grade == 12:
                grade_count[3] += 1
            if grade == 13:
                grade_count[4] += 1

    df = pandas.DataFrame({"Grade": range(9, 14), "Count": grade_count})

    print(df)

    fig = px.bar(df, x="Grade", y="Count")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


# Gráf készítése a nyelvek megoszlásáról
def language_count():
    languages = Languages.query.all()
    language_count = []
    for language in languages:
        language_count.append(Teams.query.filter_by(language=language).count())

    df = pandas.DataFrame({"Language": languages, "Count": language_count})

    fig = px.pie(df, values="Count", names="Language")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
