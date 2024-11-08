from flask import Blueprint, render_template

students = Blueprint("register", __name__, static_folder="static", template_folder="templates")

"""
Itt találhatóak a diákoknak az elérési utak,
/register - Itt tudnak a versenyre jelentkezni
/login - Itt tud valaki bejelentkezi
/modify - Itt lehet a már regisztrált csapatoknak szerkeszteni az adatait bejelentkezés után
"""

@students.route('/register')
def register():
    form = ""

@students.route('/login')
def login():
    return ""

@students.route('/modify')
def modify():
    return "a"

