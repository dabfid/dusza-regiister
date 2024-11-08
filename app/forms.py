from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

class Register(FlaskForm):
    nev = StringField("placehholder", validators=[DataRequired])
