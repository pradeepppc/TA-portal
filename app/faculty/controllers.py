from flask import Blueprint,request,session,jsonify
from flask import *
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import Faculty
from app.application.models import *
from app.student.models import *
mod_faculty=Blueprint('faculty',__name__,url_prefix='/faculty')

@mod_faculty.route('',methods=['GET'])
def check_login():
    if 'faculty_id' in session:
        faculty=Faculty.query.filter(Faculty.id==session['faculty_id']).first()
        applications = []
        applic=Application.query.filter(Application.faculty_id==session['faculty_id']).all()
        for user in applic:
            applications.append(Student.query.filter(Student.id==user.student_id).first())
        nominees=Nomination.query.filter(Nomination.faculty_id==session['faculty_id']).all()
        nominations=[]
        for user in nominees:
            nominations.append(Student.query.filter(Student.id==user.student_id).first())
        final=FinalTA.query.filter(FinalTA.faculty_id==session['faculty_id']).all()
        finaltas=[]
        for user in final:
            finaltas.append(Student.query.filter(Student.id==user.student_id).first())
        return render_template('faculty_home1.html' , message='successful' , applications=applications , nominations=nominations , finaltas=finaltas)
    return render_template('faculty_login.html')

@mod_faculty.route('',methods=['POST'])
def login():
    try:
        email = request.form['email']
        passwd = request.form['passwd']
    except KeyError as e:
        return render_template('faculty_login.html' , message = "please fill up all the fields in the form")
    faculty=Faculty.query.filter(Faculty.email==email).first()
    if faculty is None or not faculty.check_password(passwd):
        return render_template('faculty_login.html',  message="Invalid Email/Password")
    session['faculty_id']=faculty.id
    applic=Application.query.filter(Application.faculty_id==session['faculty_id']).all()
    applications=[]
    for user in applic:
        applications.append(Student.query.filter(Student.id==user.student_id).first())
    nominees=Nomination.query.filter(Nomination.faculty_id==session['faculty_id']).all()
    nominations=[]
    for user in nominees:
        nominations.append(Student.query.filter(Student.id==user.student_id).first())
    final=FinalTA.query.filter(FinalTA.faculty_id==session['faculty_id']).all()
    finaltas=[]
    for user in final:
        finaltas.append(Student.query.filter(Student.id==user.student_id).first())
    return render_template('faculty_home1.html' , message='successful' , applications=applications , nominations=nominations , finaltas=finaltas)


@mod_faculty.route('/registerpage',methods=['GET'])
def register():
    return render_template('faculty_register.html')


@mod_faculty.route('/register',methods=['POST'])
def create_faculty():
    if not request.form['name'] or not request.form['email'] or not request.form['course_id'] or not request.form['course_name'] or not request.form['course_description'] or not request.form['passwd']:
        return render_template('faculty_register.html' , message = "please fill up all the fields")
    try:
        name = request.form['name']
        email = request.form['email']
        course_id = request.form['course_id']
        course_name = request.form['course_name']
        course_description=request.form['course_description']
        passwd=request.form['passwd']
    except KeyError as e:
        return render_template('faculty_register.html' , message="please fill up all the fields")
    if '@' not in email:
        return render_template('faculty_register.html' ,message="Please enter a valid email,email should contain '@'")
    if len(course_id) != 6:
        return render_template('faculty_register.html' , message= "Please enter valid course_id")
    prof=Faculty(name,email,course_id,course_name,course_description,passwd)
    db.session.add(prof)
    try:
        db.session.commit()
    except IntegrityError as e:
        return render_template('faculty_register.html',message="This email or course-id already exists. Pls try a new one") 
    session['faculty_id']=prof.id
#    return render_template('faculty_login.html' , message = "You have been successfully regetered please login to see your account")
    return redirect(url_for('faculty.check_login'))

@mod_faculty.route('/logout',methods=['POST'])
def logout():
    if 'faculty_id' in session:
        session.pop('faculty_id')
    return render_template('home.html')
#    return redirect(url_for('faculty.check_login'))


@mod_faculty.route('/getall',methods=['GET'])
def getall():
    fac = Faculty.query.all()
    users = []
    for faculty in fac:
        u = faculty.to_dict()
        users.append(u)
    return jsonify(allfaculty = users)

@mod_faculty.route('/add' , methods=['POST'])
def add():
        student_roll = request.form['roll']
        facultyid = session['faculty_id']
        student1 = Student.query.filter(Student.rollno == student_roll).first()
        nom = Nomination(student1.id , facultyid)
        app = Application.query.filter(and_(Application.student_id == student1.id,Application.faculty_id == facultyid)).first()
        db.session.add(nom)
        db.session.delete(app)
        db.session.commit()
        applic=Application.query.filter(Application.faculty_id==session['faculty_id']).all()
        applications = []
        for user in applic:
            applications.append(Student.query.filter(Student.id==user.student_id).first())
        nominees = Nomination.query.filter(Nomination.faculty_id == facultyid).all()
        nominations=[]
        for user in nominees:
            nominations.append(Student.query.filter(Student.id==user.student_id).first())
        final=FinalTA.query.filter(FinalTA.faculty_id==session['faculty_id']).all()
        finaltas = []
        for user in final:
            finaltas.append(Student.query.filter(Student.id==user.student_id).first())
       # return render_template('faculty_home1.html' , message='successful' , applications=applications , nominations=nominations , finaltas=finaltas)
        return redirect(url_for('faculty.check_login'))
        
