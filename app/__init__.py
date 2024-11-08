from flask import Flask
app = Flask(__name__)

app.config['SECRET_KEY'] = "asd"

#database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/dusza'

from app.students import students

app.register_blueprint(students, url_prefix="/students")

if __name__ == '__main__':
    app.run()
