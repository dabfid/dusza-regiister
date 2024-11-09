from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = "asd"

#database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/dusza'

from app.students import students_bp
from app.dashboard import dashboard

app.register_blueprint(students_bp, url_prefix="/students")
app.register_blueprint(dashboard, url_prefix="/dashboard")

if __name__ == '__main__':
    app.run()
