from flask import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import *
#from app.nomination.models import *
from app.student.models import *
from app.faculty.models import *
from app.application.models import *
from sqlalchemy import *

mod_tachair = Blueprint('tachair', __name__, url_prefix='/tachair')

@mod_tachair.route('', methods=['GET'])
def check_login():
    if 'tachair_id' in session:
        user = Tachair.query.filter(Tachair.id == session['tachair_id']).first()
        alls = []
        nominations = Nomination.query.all()
        for nomi in nominations:
            rel = []
            student1 =Student.query.filter(Student.id == nomi.student_id).first()
            faculti1=Faculty.query.filter(Faculty.id == nomi.faculty_id).first()
            king = AcceptedApplication.query.filter(and_(AcceptedApplication.student_id == student1.id, AcceptedApplication.faculty_id == faculti1.id)).all()
            dicts = {
                'roll':student1.rollno,
                'name':student1.name,
                'cgpa' : student1.cgpa,
                'coursename':faculti1.course_name,
                'courseid': faculti1.course_id,
                }
            king1=FinalTA.query.filter(and_(FinalTA.student_id == student1.id,FinalTA.faculty_id == faculti1.id )).all()
            if king == []:
                if king1 == []:
                    alls.append(dicts)
        return render_template('tachair_home.html', user = user , alls = alls)

    return render_template('tachair_login.html' , message = "please login first")



@mod_tachair.route('', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return render_template('tachair_login.html',message = "Please enter all the  fields")
    user = Tachair.query.filter(Tachair.email == email).first()
    alls = []
    if user is None or not user.check_password(password):
        return render_template('tachair_login.html' , message = "Invalid credentials")
    session['tachair_id'] = user.id
    nominations = Nomination.query.all()
    for nomi in nominations:
        rel = []
        student1 =Student.query.filter(Student.id == nomi.student_id).first()
        faculti1=Faculty.query.filter(Faculty.id == nomi.faculty_id).first()
        king = AcceptedApplication.query.filter(and_(AcceptedApplication.student_id == student1.id, AcceptedApplication.faculty_id == faculti1.id)).all()
        dicts = {
                'roll':student1.rollno,
                'name':student1.name,
                'cgpa' : student1.cgpa,
                'coursename':faculti1.course_name,
                'courseid': faculti1.course_id,
                }
    
        king1=FinalTA.query.filter(and_(FinalTA.student_id == student1.id,FinalTA.faculty_id == faculti1.id )).all()
        if king == []:
            if king1 == []:
                alls.append(dicts)
    return render_template('tachair_home.html' , user = user , alls = alls)


@mod_tachair.route('/logout', methods=['POST'])
def logout():
    if 'tachair_id' in session:
        session.pop('tachair_id')
    return render_template('home.html')

@mod_tachair.route('/register' , methods=['POST'])
def regester():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = Tachair(name,email,password)
        db.session.add(user)
        db.session.commit()
        return jsonify(success = True)
    except:
        return jsonify(success = False)
@mod_tachair.route('/getall' , methods=['GET'])
def getall():
    user = Tachair.query.all()
    users = []
    for u in user:
        users.append(u.to_dict())
    return jsonify(success = True, user = users)

@mod_tachair.route('/acc', methods=['POST'])
def acc():
    try:
        user = Tachair.query.filter(Tachair.id == session['tachair_id']).first()
        student_roll = request.form['roll']
        facultyid = request.form['course_id']
        student2 = Student.query.filter(Student.rollno == student_roll).first()
        faculty2 = Faculty.query.filter(Faculty.course_id == facultyid).first()
        accep = AcceptedApplication(student2.id , faculty2.id)
        db.session.add(accep)
        db.session.commit()
        alls = []
        nominations = Nomination.query.all()
        for nomi in nominations:
            rel = []
            student1 =Student.query.filter(Student.id == nomi.student_id).first()
            faculti1=Faculty.query.filter(Faculty.id == nomi.faculty_id).first()
            king = AcceptedApplication.query.filter(and_(AcceptedApplication.student_id == student1.id, AcceptedApplication.faculty_id == faculti1.id)).all()
            dicts = {
                'roll':student1.rollno,
                'name':student1.name,
                'cgpa' : student1.cgpa,
                'coursename':faculti1.course_name,
                'courseid': faculti1.course_id,
                }
            if king == []:
                alls.append(dicts)
        #return render_template('tachair_home.html', alls =alls , user = user)
        return redirect(url_for('tachair.check_login'))
    except:
        return render_template('tachair_login.html' , message="sorry for inconvineance please login again and try")
        
