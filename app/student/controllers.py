from flask import *
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from app import db
from .models import Student
from app.faculty.models import *
from app.application.models import *
mod_student = Blueprint('student', __name__, url_prefix='/student')

@mod_student.route('', methods=['GET'])
def check_login_student():
    if 'student_id' in session:
        user = Student.query.filter(Student.id == session['student_id']).first()
        allcourses=Faculty.query.all()
        taship=FinalTA.query.filter(FinalTA.student_id==session['student_id']).all()
        if taship != []:
            faculty=Faculty.query.filter(Faculty.id==taship[0].faculty_id).first()
            return render_template('student_final.html' , faculty=faculty)
        pref=Preference.query.filter(Preference.student_id==session['student_id']).all()
        if pref==[]:
            return render_template('student_home.html', message=user.to_dict(), users = allcourses)
        preference1=Faculty.query.filter(Faculty.id==pref[0].faculty1_id).first()
        preference2=Faculty.query.filter(Faculty.id==pref[0].faculty2_id).first()
        preference3=Faculty.query.filter(Faculty.id==pref[0].faculty3_id).first()
        accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference1.id , AcceptedApplication.student_id==session['student_id'])).all()
        if accepted==[]:
            message1="Not yet accepted"
        else:
            message1="Accepted"
        accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference2.id , AcceptedApplication.student_id==session['student_id'])).all()
        if accepted==[]:
            message2="Not yet accepted"
        else:
            message2="Accepted"
        accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference3.id , AcceptedApplication.student_id==session['student_id'])).all()
        if accepted==[]:
            message3="Not yet accepted"
        else:
            message3="Accepted"
        return render_template('student_home2.html', student=user , faculty1=preference1 , faculty2=preference2 , faculty3=preference3 ,message1=message1 , message2=message2 , message3=message3)
    return render_template('student_login.html')

 
@mod_student.route('', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        return render_template('student_login.html',message = "Please enter all the  fields")

    user = Student.query.filter(Student.email == email).first()
    if user is None or not user.check_password(password):
        return render_template('student_login.html' , message = "Invalid credentials")
    session['student_id'] = user.id
    taship=FinalTA.query.filter(FinalTA.student_id==session['student_id']).all()
    if taship != []:
        faculty=Faculty.query.filter(Faculty.id==taship[0].faculty_id).first()
        return render_template('student_final.html' , faculty=faculty)
    allcourses = Faculty.query.all()
    pref=Preference.query.filter(Preference.student_id==session['student_id']).all()
    if pref==[]:
        return render_template('student_home.html', message=user.to_dict(), users = allcourses)
    preference1=Faculty.query.filter(Faculty.id==pref[0].faculty1_id).first()
    preference2=Faculty.query.filter(Faculty.id==pref[0].faculty2_id).first()
    preference3=Faculty.query.filter(Faculty.id==pref[0].faculty3_id).first()
    accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference1.id , AcceptedApplication.student_id==session['student_id'])).all()
    if accepted==[]:
        message1="Not yet accepted"
    else:
        message1="Accepted"
    accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference2.id , AcceptedApplication.student_id==session['student_id'])).all()
    if accepted==[]:
        message2="Not yet accepted"
    else:
        message2="Accepted"
    accepted=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==preference3.id , AcceptedApplication.student_id==session['student_id'])).all()
    if accepted==[]:
        message3="Not yet accepted"
    else:
        message3="Accepted"
    return render_template('student_home2.html', student=user , faculty1=preference1 , faculty2=preference2 , faculty3=preference3 ,message1=message1 , message2=message2 , message3=message3)


@mod_student.route('/registerpage',methods=['GET'])
def registerpage():
    return render_template('student_register.html')


@mod_student.route('/logout', methods=['POST'])
def logout():
    if 'student_id' in session:
        session.pop('student_id')
    return render_template('home.html')


@mod_student.route('/register', methods=['POST'])
def create_student():
    try:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cgpa  = request.form['cgpa']
        rollno = request.form['rollno']
    except KeyError as e:
        return render_template('student_register.html',message="please fill all the fields")


    if '@' not in email:
        return render_template('student_register.html' , message = "please enter valid email address")
    if  float(cgpa) <= 0 or float(cgpa) >= 10:
        return render_template('student_register.html' , message="please enter valid cgpa")  
    if int(rollno) >= 20169999 or int(rollno) <= 20120000:
        return render_template('student_register.html' , message="please enter valid roll number")     
    u = Student(name, email, cgpa , rollno , password)
    db.session.add(u)
    try:
        db.session.commit()
    except IntegrityError as e:
        return render_template('student_register.html', message="This email or roll number already exists")
    session['student_id']=u.id
    return redirect(url_for('student.check_login_student'))
@mod_student.route('/getall' , methods=['GET'])
def getall():
    students = Student.query.all()
    users1 = []
    for student in students:
        users1.append(student.to_dict())
    applications=Application.query.all()
    users2 = []
    for application in applications:
        users2.append(application.to_dict())    
    nominations=Nomination.query.all()
    users3 = []
    for nomination in nominations:
        users3.append(nomination.to_dict())    
    acceptedapplications=AcceptedApplication.query.all()
    users4 = []
    for acceptedapplication in acceptedapplications:
        users4.append(application.to_dict())    
    finalta=FinalTA.query.all()
    users5 = []
    for a in finalta:
        users5.append(a.to_dict())    
    f=Faculty.query.all()
    users6 = []
    for a in f:
        users6.append(a.to_dict())    
    return jsonify(students= users1,applications=users2,nomination=users3,acceptedapplications=users4,finalta=users5,faculty=users6)

@mod_student.route('/addpreference',methods=['POST'])
def create_preference():
    try:
        course1_id=request.form['course1_id']
        course2_id=request.form['course2_id']
        course3_id=request.form['course3_id']
    
    except KeyError as e:
        return render_template('student_home.html', message="please fill all the preferences")
    
    stud=Student.query.filter(Student.id==session['student_id']).first()
    preference1=Faculty.query.filter(Faculty.course_id==course1_id).first()
    preference2=Faculty.query.filter(Faculty.course_id==course2_id).first()
    preference3=Faculty.query.filter(Faculty.course_id==course3_id).first()
    pref=Preference(session['student_id'],preference1.id,preference2.id,preference3.id)
    app1=Application(session['student_id'],preference1.id)
    app2=Application(session['student_id'],preference2.id)
    app3=Application(session['student_id'],preference3.id) 
    try:
        db.session.add(pref)
        db.session.add(app1)
        db.session.add(app2)
        db.session.add(app3)
        db.session.commit()
    except IntegrityError as e:
        return render_template('student_home.html', message="Sorry Request Failed")
    return redirect(url_for('student.check_login_student'))

@mod_student.route('/addfinalta',methods=['POST'])
def create_finalta():
    user=Student.query.filter(Student.id==session['student_id']).all()
    pref=Preference.query.filter(Preference.student_id==session['student_id']).all()
    if pref==[]:
        return render_template('student_home.html', message=user.to_dict(), users = allcourses)
    preference1=Faculty.query.filter(Faculty.id==pref[0].faculty1_id).first()
    preference2=Faculty.query.filter(Faculty.id==pref[0].faculty2_id).first()
    preference3=Faculty.query.filter(Faculty.id==pref[0].faculty3_id).first()
    accepted=AcceptedApplication.query.filter(AcceptedApplication.faculty_id==preference1.id).all()
    if accepted==[]:
        message1="Not yet accepted"
    else:
        message1="Accepted"
    accepted=AcceptedApplication.query.filter(AcceptedApplication.faculty_id==preference2.id).all()
    if accepted==[]:
        message2="Not yet accepted"
    else:
        message2="Accepted"
    accepted=AcceptedApplication.query.filter(AcceptedApplication.faculty_id==preference3.id).all()
    if accepted==[]:
        message3="Not yet accepted"
    else:
        message3="Accepted"
    try:
        course_id=request.form['faculty_id']
        faculty_id=Faculty.query.filter(Faculty.course_id==course_id).first().id
    except KeyError as e:
        return render_template('student_home2.html', message="form not going" , student=user , faculty1=preference1 , faculty2=preference2 , faculty3=preference3 ,message1=message1 , message2=message2 , message3=message3)
    array=AcceptedApplication.query.filter(and_(AcceptedApplication.faculty_id==faculty_id,AcceptedApplication.student_id==session['student_id'])).all()
    finalta=FinalTA(array[0].student_id,array[0].faculty_id)
    try:
        db.session.add(finalta)
        db.session.delete(array[0])
        db.session.commit()
    except IntegrityError as e:
        return render_template('student_home2.html', message="Request Failed" , student=user , faculty1=preference1 , faculty2=preference2 , faculty3=preference3 ,message1=message1 , message2=message2 , message3=message3)
    return redirect(url_for('student.check_login_student'))
        

