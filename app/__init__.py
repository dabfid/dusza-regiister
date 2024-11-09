from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = "asd"

#database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/dusza'

from app.students import students
from app.dashboard import dashboard

app.register_blueprint(students, url_prefix="/students")
app.register_blueprint(dashboard, url_prefix="/dashboard")

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)
        exit(1)
