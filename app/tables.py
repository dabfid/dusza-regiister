from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT

from werkzeug.security import generate_password_hash, check_password_hash

from flask_migrate import Migrate

from app import app # pyright: ignore

"""
Itt vannak az SQLAlchemy számára a táblák definiálva.
"""

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Schools(db.Model):
    """
    Iskolák tárolása.
    """
    __tablename__ = "schools"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(200), unique=True, nullable=False, index=True)

class Admins(db.Model):
    """
    szervező felhasználók tárolása.
    """
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
    """
    Programozási nyelvek tárolása.
    """
    __tablename__ = "languages"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), unique=True, index=True)

class Categories(db.Model):
    """
    Verseny kategóriák tárolása.
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(TEXT, nullable=False)

class Teams(db.Model):
    """
    A jelentkezett csapat adatainak tárloása.
    """
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(30), nullable=False, index=True)

    email = db.Column(db.String(60), nullable=False, unique=True)

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

    teachers = db.Column(TEXT, nullable=False)
    
    category = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    language = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)

    is_valid = db.Column(db.Boolean, default=False)

class Notifications(db.Model):
    """
    Értesítések tárolása.
    """
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True, index=True)
    message = db.Column(TEXT, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)

