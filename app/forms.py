from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField, EmailField
from wtforms.validators import DataRequired, Email
from wtforms.validators import Length

from flask_wtf import FlaskForm

from app.tables import Schools, Categories, Languages

class RegisterForm(FlaskForm):
    """
    Ez a form szolgál a versenyre való jelentkezeésre.
    """

   # Ezekkel az adatokkal lehet késöbb szerkeszteni a megadott adatokat
    username = StringField("Felhasználónév:", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Jelszó:", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("Jelszó megerősítése:", validators=[DataRequired(), Length(max=30)])
    email = EmailField("Email cím:", validators=[DataRequired(), Length(max=60)])
    # Csapat Adatai
    team_name = StringField("Csapat neve:", validators=[DataRequired(), Length(max=30)])
    school = SelectField("Iskola neve:", validators=[DataRequired()], coerce=int)

    teammate1 = StringField("Első csapattag neve:", validators=[DataRequired(), Length(max=30)])
    grade1 = SelectField("Első csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate2 = StringField("Második csapattag neve:", validators=[DataRequired(), Length(max=30)])
    grade2 = SelectField("Második csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate3 = StringField("Harmadik csapattag neve:", validators=[DataRequired(), Length(max=30)])
    grade3 = SelectField("Harmadik csapattag osztály:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    # póttag
    extra_teammate = StringField("Extra csapattag neve:", validators=[Length(max=30)])
    extra_grade = SelectField("Extra cspattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[])

    teachers = StringField("Felkészítő tanár:", validators=[DataRequired()])

    category = SelectField("Versenykategória:", validators=[DataRequired()], coerce=int)
    language = SelectField("Választott programozási nyelv:", validators=[DataRequired()], coerce=int)

    submit = SubmitField("Küldés")

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
    team_name = StringField("Új csapatnév:", validators=[DataRequired(), Length(max=30)])
    school = SelectField('Iskola megváltoztatása:', validators=[DataRequired()], coerce=int)

    teammate1 = StringField("1. csapattag megváltoztatása:", validators=[DataRequired(), Length(max=30)])
    grade1 = SelectField("Új csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate2 = StringField("2. csapattag megváltoztatása:", validators=[DataRequired(), Length(max=30)])
    grade2 = SelectField("Új csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    teammate3 = StringField("3. csapattag megváltoztatása:", validators=[DataRequired(), Length(max=30)])
    grade3 = SelectField("Új csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[DataRequired()])

    # póttag
    extra_teammate = StringField("Extra csapattag megváltoztatása:", validators=[Length(max=30)])
    extra_grade = SelectField("Új csapattag osztálya:", choices=[(9, "9"), (10, "10"), (11, "11"), (12, "12"), (13, "13")], validators=[])

    teachers = StringField("Felkészítő tanár megváltoztatása:", validators=[DataRequired()])

    category = SelectField('Kategória megváltoztatása:', validators=[DataRequired()], coerce=int)
    language = SelectField('Nyelv megváltoztatása:', validators=[DataRequired()], coerce=int)

    submit = SubmitField("Küldés")

    def __init__(self, *args, **kwargs):
        super(UpdateForm, self).__init__(*args, **kwargs)
        self.school.choices = [(school.id, school.name) for school in Schools.query.all()]
        self.category.choices = [(category.id, category.name) for category in Categories.query.all()]
        self.language.choices = [(language.id, language.name) for language in Languages.query.all()]


class LoginForm(FlaskForm):
    """
    Bejelentkezéshez használt form, szervezők, iskolák és a sima felhasználók is ezt használják.
    """

    username = StringField("Felhasználónév:", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Jelszó:", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("Bejelentkezés")

class AddLanguageForm(FlaskForm):
    """
    Új programozási nyelv hozzáadásához használt form.
    """
    language = StringField("Nyelv hozzáadása:", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Hozzáadás")

class AddCategoryForm(FlaskForm):
    """
    Új kategória hozzáadásához használt form.
    """
    category = StringField("Kategória:", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Hozzáadás")

class AddSchoolForm(FlaskForm):
    """
    Új iskola hozzáadásához használt form.
    """
    username = StringField("Felhasználónév:", validators=[DataRequired(), Length(max=30)])
    
    password = PasswordField("Jelszó:", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("Jelszó megerősítése:", validators=[DataRequired(), Length(max=30)])

    contact_name = StringField("Kapcsolattartó neve:", validators=[DataRequired(), Length(max=30)])
    contact_email = EmailField("Kapcsolattartó e-mail címe:", validators=[DataRequired(), Length(max=60)])

    school_name = StringField("Iskola neve:", validators=[DataRequired(), Length(max=30)])
    school_address = StringField("Iskola címe:", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("Hozzáadás")

class UpdateSchoolForm(FlaskForm):
    """
    Meglévő iskola adatainak módosításához használt form.
    """
    contact_name = StringField("Új kapcsolattartó neve:", validators=[DataRequired(), Length(max=30)])
    contact_email = EmailField("Új kapcsolattartó e-mail címe:", validators=[DataRequired(), Length(max=60)])

    school_name = StringField("Iskola megváltoztatott neve", validators=[DataRequired(), Length(max=30)])
    school_address = StringField("Iskola megváltoztatott címe:", validators=[DataRequired(), Length(max=30)])

    submit = SubmitField("Frissítés")

class ValidateTeamForm(FlaskForm):
    """
    Csapatok validálására használt form.
    """
    submit = SubmitField("")

class ModifyDeadlineForm(FlaskForm):
    """
    Határidő módosítására használt form.
    """
    deadline = DateTimeField("Új határidő:", validators=[DataRequired()])
    submit = SubmitField("Beállítás")

class RegisterNewAdminForm(FlaskForm):
    """
    Új adminisztrátor hozzáadására használt form.
    """
    username = StringField("Felhasználónév:", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("Jelszó:", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("Jelzó egerősítése:", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Regisztrálás")

class ChangePasswordForm(FlaskForm):
    """
    Adminisztrátor jelszavának módosítására használt form.
    """
    old_password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    confirm_password = PasswordField("", validators=[DataRequired(), Length(max=30)])
    submit = SubmitField("Módosítás")
