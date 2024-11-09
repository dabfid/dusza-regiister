from flask import Flask, Blueprint, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tables import Languages, db, Categories
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import  DataRequired
from forms import AddLanguageForm, AddCategoryForm

dashboard_blueprint = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")


#delete elements from database
@dashboard_blueprint.route("/delete_language/<int:item_id>", methods=["POST"])
def delete_element(item_id):
    item = Languages.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("languages"))


@dashboard_blueprint.route("/delete_category/<int:item_id>", methods=["POST"])
def delete_element(item_id):
    item = Categories.query.get(item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for("categories"))

   


@dashboard_blueprint.route("/", methods=['GET'])
def dashboard():
    if session["permission"] == "admin":
        return render_template("dashboard.html")



#language page
dashboard_blueprint.route("/languages", methods=['GET', 'POST'])
def languages():

    form = AddLanguageForm()
    language: str = None
    result = Languages.query.all

    if form.validate_on_submit():
        language = form.language.data
        new_language = Languages(name=language)
        db.session.add(new_language)
        db.session.commit()
        form.language.data = ""



    return render_template("languages.html", language = language, form = form, list = result)




#categories page
dashboard_blueprint.route("/categories", methods=['GET', 'POST'])
def categories():

    form = AddCategoryForm()
    category: str = None
    result = Categories.query.all

    if form.validate_on_submit():
        category = form.categorie.data
        new_category = Categories(name=category)
        db.session.add(new_category)
        db.session.commit()
        form.category.data = ""



    return render_template("categories.html", category = category, form = form, list = result)