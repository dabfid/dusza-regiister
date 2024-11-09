from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length

from flask_wtf import FlaskForm

from app.tables import Schools, Categories, Languages

class RegisterForm(FlaskForm):
    """
    Ez a form szolgál a versenyre való jelentkezeésre.
    """

   # Ezekkel az adatokkal lehet késöbb szerkeszteni a megadott adatokat
    username = StringField("", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    email = StringField("", validators=[DataRequired(), Email(), Length(max=60)])

    # Csapat Adatai
    team_name = StringField("", validators=[DataRequired(), Length(max=30)])
    school = SelectField('Iskola', validators=[DataRequired()], coerce=int)

    teammate1 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade1 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate2 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade2 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate3 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade3 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    # póttag
    extra_teammate = StringField("", validators=[Length(max=30)])
    extra_grade = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[])

    teachers = StringField("", validators=[DataRequired()])

    category = SelectField('Kategória', validators=[DataRequired()], coerce=int)
    language = SelectField('Nyelv', validators=[DataRequired()], coerce=int)

    submit = SubmitField("")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.school.choices = [(school.id, school.name) for school in Schools.query.all()]
        self.category.choices = [(category.id, category.name) for category in Categories.query.all()]
        self.language.choices = [(language.id, language.name) for language in Languages.query.all()]

class UpdateForm(FlaskForm):
    """
    Ez a form szolgál a versenyzők adatainak módosítására. 
    """

    email = StringField("", validators=[DataRequired(), Email(), Length(max=60)])

    # Csapat Adatai
    team_name = StringField("", validators=[DataRequired(), Length(max=30)])
    school = SelectField('Iskola', validators=[DataRequired()], coerce=int)

    teammate1 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade1 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate2 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade2 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate3 = StringField("", validators=[DataRequired(), Length(max=30)])
    grade3 = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    # póttag
    extra_teammate = StringField("", validators=[Length(max=30)])
    extra_grade = SelectField("", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[])

    teachers = StringField("", validators=[DataRequired()])

    category = SelectField('Kategória', validators=[DataRequired()], coerce=int)
    language = SelectField('Nyelv', validators=[DataRequired()], coerce=int)

    submit = SubmitField("")

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.school.choices = [(school.id, school.name) for school in Schools.query.all()]
        self.category.choices = [(category.id, category.name) for category in Categories.query.all()]
        self.language.choices = [(language.id, language.name) for language in Languages.query.all()]


class LoginForm(FlaskForm):
    """
    Bejelentkezéshez használt form, szervezők, iskolák és a sima felhasználók is ezt használják.
    """

    username = StringField("", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("")

class AddLanguageForm(FlaskForm):
    """
    Új programozási nyelv hozzáadásához használt form.
    """
    language = StringField("Nyelv hozzáadása:", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("")

class AddCategoryForm(FlaskForm):
    """
    Új kategória hozzáadásához használt form.
    """
    category = StringField("", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("")

class AddSchoolForm(FlaskForm):
    """
    Új iskola hozzáadásához használt form.
    """
    username = StringField("", validators=[DataRequired(), Length(max=30)])
    
    password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("", validators=[DataRequired(), Length(max=30)])

    contact_name = StringField("", validators=[DataRequired(), Length(max=30)])
    contact_email = StringField("", validators=[DataRequired(), Email(), Length(max=60)])

    school_name = StringField("", validators=[DataRequired(), Length(max=30)])
    school_address = StringField("", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("")

class UpdateSchoolForm(FlaskForm):
    """
    Meglévő iskola adatainak módosításához használt form.
    """
    contact_name = StringField("", validators=[DataRequired(), Length(max=30)])
    contact_email = StringField("", validators=[DataRequired(), Email(), Length(max=60)])

    school_name = StringField("", validators=[DataRequired(), Length(max=30)])
    school_address = StringField("", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("")

class ValidateTeamForm(FlaskForm):
    """
    Csapatok validálására használt form.
    """
    submit = SubmitField("")

