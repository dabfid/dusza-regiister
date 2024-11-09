from flask import Blueprint, render_template, flash
from app.tables import Teams #pyright: ignore
from app.tables import db #pyright: ignore

from app.forms import RegisterForm, UpdateForm #pyright: ignore

students = Blueprint("students_bp", __name__, static_folder="static", template_folder="templates")

"""
A jelentkező diákokhoz tartozó route-okat tartalmazó blueprint.
"""

@students.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    username = None
    password = None
    confirm_password = None
    email = None

    team_name = None

    school = None

    t1 = None #csapatárs 1
    t2 = None #csapatárs 2
    t3 = None #csapatárs 3
    g1 = None #csapatárs 1 évfolyama
    g2 = None #csapatárs 2 évfolyama
    g3 = None #csapatárs 3 évfolyama

    t_extra = None #pót csapatárs
    g_extra = None #pót csapatárs évfolyama

    teachers = None

    category = None
    language = None

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

        if (form.extra_teammate.data): 
            t_extra = form.extra_teammate.data

        if (form.extra_grade): 
            g_extra = form.extra_grade.data

        teachers = form.teachers.data

        category = form.category.data
        language = form.language.data

        if (confirm_password != password):
            pass #do stuff!!

        new_team = Teams(
                username=username,
                password=password,
                email=email,
                team_name=team_name,
                school_id=school,
                teammate1=t1,
                teammate2=t2,
                teammate3=t3,
                grade1=g1,
                grade2=g2,
                grade3=g3,
                teammate_extra=t_extra,
                grade_extra=g_extra,
                teachers=teachers,
                category=category,
                language=language
                )
        db.session.add(new_team)
        db.session.commit()
        return "succes!"
    return "a"

@students.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    form = UpdateForm()
    team = Teams.query.get_or_404(id)
    
    if form.validate_on_submit():
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
            flash('Verseny adatok sikeresen frissítve!')
            return render_template('edit.html', form=form, team=team)
        except:
            flash('Hiba történt a frissítés során!')
            return render_template('edit.html', form=form, team=team)
    return render_template('edit.html', form=form, team=team)
