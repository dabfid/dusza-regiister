from flask import Blueprint, render_template, request

from app.tables import Teams
from app.tables import db

from app.forms import RegisterForm

students = Blueprint("students_bp", __name__, static_folder="static", template_folder="templates")

@students.route('/register', methods=['GET', 'POST'])
def register_new_team():
    if request.method == 'POST':
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
        return "invalid form"
    return "a"

@students.route('/edit')
def edit():
    return "a"

@students.route('/modify')
def modify():
    return "a"
