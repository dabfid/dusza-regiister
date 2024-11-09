from flask import Flask, Blueprint, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Languages, db
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired
from forms import AddLanguageForm

dashboard_blueprint = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")



@dashboard_blueprint.route("/", methods=['GET'])
def dashboard():
    if session["permission"] == "admin":
        return render_template("dashboard.html")


dashboard_blueprint.route("/languages", methods=['GET', 'POST'])
def languages():
    form = AddLanguageForm()
    language: str = None

    if form.validate_on_submit():
        language = form.language.data
        return render_template("languages.html", content = language)

    return render_template("languages.html", language = language, form = form)
