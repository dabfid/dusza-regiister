from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT

from werkzeug.security import generate_password_hash, check_password_hash

from app import app

"""
Itt vannak az SQLAlchemy számára a táblák definiálva.
"""

db = SQLAlchemy(app)

class Schools(db.Model):
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)

class Admins(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(30), nullable=False, index=True)

    @property
    def password(self):
        raise AttributeError("Warning you cannot directly access the password of a user")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

class Languages(db.Model):
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), unique=True, index=True)

class Categories(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(TEXT, nullable=False)

class Students(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(30), nullable=False, index=True)


class Teams(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, index=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))

    @property
    def password(self):
        raise AttributeError("Warning you cannot directly access the password of a user")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    team_name = db.Column(db.String(30), unique=True, nullable=False)

    school_id = db.Column(db.Integer, db.ForeignKey('schools.id'), nullable=False)
    
    teammate1 = db.Column(db.String(30), nullable=False)
    grade1 = db.Column(db.Integer, nullable=False)
    teammate2 = db.Column(db.String(30), nullable=False)
    grade2 = db.Column(db.Integer, nullable=False)
    teammate3 = db.Column(db.String(30), nullable=False)
    grade3 = db.Column(db.Integer, nullable=False)

    teammate_extra = db.Column(db.String(30))
    grade_extra = db.Column(db.Integer)

    teachers = db.Column(db.String(TEXT, nullable=False))
    
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    language = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

