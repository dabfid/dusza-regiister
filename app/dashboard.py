from flask import Flask, Blueprint, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Languages, db

dashboard_blueprint = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")



@dashboard_blueprint.route("/", methods=['GET'])
def dashboard():
    if session["permission"] == "admin":
        return render_template("dashboard.html")


dashboard_blueprint.route("/languages", methods=['GET', 'POST'])
def languages():
    if request.method == 'GET' and session["permission"] == "admin":
        return render_template("languages.html")
    if request.method == 'POST':
        language: str = request.form("language")
        
        new_language = Languages(name=language)
        db.session.add(new_language)
        db.session.commit()
