################################
# import all things from flask #
################################
from flask import *
#####################
# Import SQLAlchemy #
#####################
from flask_sqlalchemy import SQLAlchemy

from functools import wraps

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 200
###########################
#add security so as to fin#
###########################
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify(message="Unauthorized", success=False), 401
        return f(*args, **kwargs)
    return decorated
# Import module using blueprint
from app.student.controllers import mod_student
from app.faculty.controllers import mod_faculty
from app.tachair.controllers import mod_tachair
#################################
#   Registers the Blueprints    #
#################################
app.register_blueprint(mod_student)
app.register_blueprint(mod_faculty)
app.register_blueprint(mod_tachair)
#this creates all the tables in the data base 
db.create_all()

@app.route('/faculty')
def main():
    return render_template('faculty_login.html')
@app.route('/student')
def main1():
    return render_template('student_login.html')
@app.route('/tachair')
def main3():
    return render_template('tachair_login.html')
@app.route('/')
def main4():
    return render_template('home.html')
