from flask import Flask, render_template, g
app = Flask(__name__)

app.config['SECRET_KEY'] = "asd"

#database settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123@localhost/dusza'

from app.students import students
from app.dashboard import dashboard
from app.schools import schools

app.register_blueprint(students, url_prefix="/students")
app.register_blueprint(dashboard, url_prefix="/dashboard")
app.register_blueprint(schools, url_prefix="/schools")

@app.before_request
def load_user_info():
    g.user = None
    g.perms = 0

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

if __name__ == '__main__':
    try:
        app.run()
    except Exception as e:
        print(e)
        exit(1)
