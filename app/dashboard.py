from flask import Flask, Blueprint, render_template, request, session

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from app.tables import Languages, db # pyright: ignore

dashboard = Blueprint("dashboard_bp", __name__, 
                      static_folder="static", 
                      template_folder="templates")

@dashboard.route("/", methods=['GET'])
def dashboard():
    if session["permission"] == "admin":
        return render_template("dashboard.html")


dashboard.route("/languages", methods=['GET', 'POST'])
def languages():
    if request.method == 'GET' and session["permission"] == "admin":
        return render_template("languages.html")
    if request.method == 'POST':
        language: str = request.form("language")
        
        new_language = Languages(name=language)
        db.session.add(new_language)
        db.session.commit()
