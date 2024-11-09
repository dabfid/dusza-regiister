from flask import Blueprint, render_template, request, session, abort, url_for, redirect, flash

from flask_login import LoginManager
from flask_login import login_required, login_user, logout_user

from datetime import datetime

from app.tables import Languages, Admins, Teams, db # pyright: ignore
from app.forms import LoginForm # pyright: ignore
from app import app # pyright: ignore

import plotly
import plotly.express as px
import json
import numpy as np
import pandas

dashboard = Blueprint("dashboard_bp", __name__, static_folder="static", template_folder="templates")

# Login manager handler
login_admin = LoginManager()
login_admin.init_app(app)
login_admin.login_view = "dashboard_bp.login"

@login_admin.user_loader
def load_user(user_id):
    return Admins.query.get_or_404(user_id)

@dashboard.route("/", methods=['GET'])
@login_required
def index():
    return render_template("dashboard.html")

@dashboard.route('/login', methods=['GET', 'POST'])
def login():
    """"
    next = request.args.get("next")
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = Admins.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        if user.check_password(password):
            login_user(user)
            return redirect(next or url_for("dashboard_bp.index"))
        else:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)
      """
    login_user(Admins.query.get(1))
    next = request.args.get("next")
    return redirect(next or url_for("dashboard_bp.index"))

@dashboard.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("dashboard_bp.login"))

@dashboard.route("/languages", methods=['GET', 'POST'])
@login_required
def languages():
    if request.method == 'GET' and session["permission"] == "admin":
        return render_template("languages.html")
    if request.method == 'POST':
        language: str = request.form("language")
        
        new_language = Languages(name=language)
        db.session.add(new_language)
        db.session.commit()

@dashboard.route('/statistics', methods=['GET'])
@login_required
def statistics():
    return render_template("statistics.html", graphJSON=language_count())

# Gráf készítése a csapatok számáról
def team_count():
    teams = Teams.query.with_entities(Teams.grade1, Teams.grade2, Teams.grade3, Teams.grade_extra).all()
    grade_count = [0, 0, 0, 0, 0]
    for team in teams:
        for grade in team:
            if (grade == 9): grade_count[0] += 1
            if (grade == 10): grade_count[1] += 1
            if (grade == 11): grade_count[2] += 1
            if (grade == 12): grade_count[3] += 1
            if (grade == 13): grade_count[4] += 1

    df = pandas.DataFrame({
    'Grade': range(9, 14),
    'Count': grade_count
    })

    print(df)

    fig = px.bar(df, x='Grade', y='Count')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Gráf készítése a nyelvek megoszlásáról
def language_count():
    languages = Languages.query.all()
    language_count = []
    for language in languages:
        language_count.append(Teams.query.filter_by(language=language).count())

    df = pandas.DataFrame({
    'Language': languages,
    'Count': language_count
    })

    fig = px.pie(df, values='Count', names='Language')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

