#+TITLE: =TA-PORTAL-1=
#+AUTHOR: Pradeep.P,Sandeep.K,Harsha.G
#+SETUPFILE: ../../org-templates/level-2.org
#+EXCLUDE_TAGS: boilerplate
#+PROPERTY: session *python*
#+PROPERTY: results output
#+PROPERTY: exports code
#+TAGS: boilerplate(b) notes(n) solution(s)



* INTRODUCTION
** purpose of this document
- In this documentation there is overall description of the project and how to setup this in user interface and to use it.
- Whole description of the designing face and cost is included in this document .
** Project experiences 
- The main experience we learn from this project is to work in group , and we also learn how to create a website and host it on
  the server . 
** About project 
- This web application is called TA-SHIP portal . This is used for allocating ta's to particular courses available for the semester. 
- This web application is build using =flask sql-alchemy= for creating database  , =python= for backend using =jinja rendertemplates= 
   and javascript at front end.
** Requirements to run this project in your environment
- This project needs to setup linux environament with python , flask modules installed.
- Please run the command =pip install requirements.txt= in the folder so as to install all modules required for webapplication to run.

** How to Deploy and use
- Follow the below steps to deploy and make https certificate .
- We are using nginx for deployment.So please ensure that all the requirements for runnning nginx is installed before.
- run =pip install requirements.txt= .This command will ensure that all the modules required for running the application are installed.
- Go to the directory TA-PORTAL-1.
- type the following command
- =vim /etc/nginx/sites-available/default= and paste the given code block in that file and please make 
  sure you entered your correct server domain (or IP)
#+BEGIN_SRC python 
server {
    listen 80; 
    listen 443 ssl;
    server_name server domain or IP; #(should be IP-address of the host network)
    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;

    location / { 
        include uwsgi_params;
        uwsgi_pass unix:/home/harsha/TA-Portal-1/TA-Portal-1.sock;
    }   
}
#+END_SRC
- =uwsgi --ini TA-Portal-1=
- =sudo server nginx restart= 
- Go to browser and open the url =https://<server domain or IP(used to host)>=
* Code
** Directory structure
- This is the directory structure we have used to build the application . 
#+NAME: directory_structure
#+BEGIN_SRC python 

.
    app
        application
            __init__.py
            __init__.pyc
            models.py
            models.pyc
        faculty
            controllers.py
            controllers.pyc
            __init__.py
            __init__.pyc
            models.py
            models.pyc
        __init__.py
        __init__.pyc
        static
            css
                vendor
                    bootstrap.min.css
            js
                faculty_login.js
                faculty_register.js
                student_login.js
                student_register.js
                vendor
                    authmanger.js
                    bootstrap.min.js
                    handlebars.min.js
                    jquery.min.js
                    page.js
        student
            controllers.py
            controllers.pyc
            __init__.py
            __init__.pyc
            models.py
            models.pyc
        tachair
            controllers.py
            controllers.pyc
            __init__.py
            __init__.pyc
            models.py
            models.pyc
        templates
            book.gif
            error.html
            faculty_home1.html
            faculty_login.html
            faculty_register.html
            home.html
            IIIT-H.png
            login.html
            student_final.html
            student_home2.html
            student_home.html
            student_login.html
            student_register.html
            tachair_home.html
            tachair_login.html
    app.db
    a.txt
    config.py
    config.pyc
    databaseSchema.png
    database_schema.txt
    main.org
    README.md
    run.py
    tachairinit
        regester.html



#+END_SRC 
*** Explanation 
- 
** DATABASE
- As database is the important part of our web application we first introduce our database models to you and the table relationships 
  between them.
*** Models
**** Student
- =Student= model defines a student in our web-application .
- =Student=  model is a table in the database which has the following fields  =name= , =email= , =password= , =cgpa= , =rollno= .
- =name= field is a string having no other constraints on it , =email= and =roolno= (rollnumber) fields should be unique , i.e no two 
  students can have same =email= or =rollno= .
- In database the password is not stored directly but its hash value is stored .
- While login the form password is again hashed and is checked with this value .
- The code for =Student= model is like this
#+BEGIN_SRC python 
class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    cgpa = db.Column(db.Float)
    rollno =db.Column(db.Integer,unique = True)

    def __init__(self,name,email,cgpa,rollno,password):
        self.name = name
        self.email = email
        self.cgpa = cgpa
        self.rollno = rollno
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    def to_dict(self):
        return {
            'id' : self.id,
            'name': self.name,
            'email': self.email,
            'cgpa' : self.cgpa,
            'rollno': self.rollno,
        }
    def __repr__(self):
        return "Student<%d> %s" % (self.id, self.name)



#+END_SRC
***** functionality
- =student= implies students , they have to login and select the course_preferences inorder to apply for TA-SHIP .
- once they have submitted their preferences ,they have to wait until they got accepted by =proffesor= and =TAcahir= .
- If he or she got accepted by both  =TA-CHAIR= and =Faculty=  then the student must accept that inorder to become a TA for that particular
  subject.
- once he or she accepts the TA-SHIP it will be desplayed on his home page.
**** Faculty
- =Faculty= model defines a Faculty in our web application.
- =Faculty= model is a table in the database which has the following fields =name= (name of prof) , =email= , =course_id= (id of the course)
  , =course_name= , =course_description= , =passwd= .
- =email= and =course_id= are unique i.e no two faculty  members can have same =email= and =course_id= .
- The code for the =Faculty= model is 
#+BEGIN_SRC python
class Faculty(db.Model):
    __tablename__="faculty"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String(255))
    email=db.Column(db.String(255),unique=True)
    course_id=db.Column(db.String(6),unique=True)
    course_name=db.Column(db.String(255))
    course_description=db.Column(db.String(1000))
    passwd=db.Column(db.String(255))

    def __init__(self,name,email,course_id,course_name,course_description,passwd):
        self.name=name
        self.email=email
        self.course_id=course_id
        self.course_name=course_name
        self.course_description=course_description
        self.passwd=generate_password_hash(passwd)
    def check_password(self, passwd):
        return check_password_hash(self.passwd, passwd)
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'course_id':self.course_id,
            'course_name':self.course_name,
            'course_description':self.course_description,
        }
        def __repr__(self):
            return "Faculty<%d> %s" %(self.id,self.name)


#+END_SRC
**** Preference
- =Preference= table is used to store the data of the preferences selected by a particular student. 
- =Preference= model is a table in the database which has the following fields :
                                                                               1) =student_id= foreign_key from student table.
									       2) =faculty1_id= foreign_key from faculty table.(first preference of student) 
									       3) =faculty2_id= foreign_key from faculty table.(second preference of student)	    
  									       4) =faculty3_id= foreign_key form faculty table.(third preference of student)
- The code for =Preference= table is
#+BEGIN_SRC python

class Preference(db.Model):
    __tablename__= 'preference'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    faculty1_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))
    faculty2_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))
    faculty3_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))

    def __init__(self,student_id,faculty1_id,faculty2_id,faculty3_id):
        self.student_id=student_id
        self.faculty1_id=faculty1_id
        self.faculty2_id=faculty2_id
        self.faculty3_id=faculty3_id


#+END_SRC
**** Application
- =Application= table stores  the data of the  applications for a particular subject .
- It contains the following fields 1) =student_id= foreign_key from student table.
                                   2) =faculty_id= foreign_key from faculty table.
- It actually stores id's so inorder to get the actual =Student= and =Faculty= corresponding to that id's we have to query on database . 
- The code for =Application= table is 
#+BEGIN_SRC python

class Application(db.Model):
    __tablename__= 'application'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))

    def __init__(self,student_id,faculty_id):
        self.student_id=student_id
        self.faculty_id=faculty_id

    def to_dict(self):
        return {
            'id' : self.id,
            'student_id': self.student_id,
            'faculty_id': self.faculty_id,
        }

#+END_SRC
**** Nomination
- =Nomination= table stores the data of the students which are accepted by the professor among all the applications corresponding to that 
  subject.
- It contain the following fields 1) =student_id= (which stores the student_id)
                                  2) =faculty_id= (which stores the faculty_id)
- The code for =Nomination= table is
#+BEGIN_SRC python
class Nomination(db.Model):
    __tablename__= 'nomination'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))

    def __init__(self,student_id,faculty_id):
        self.student_id=student_id
        self.faculty_id=faculty_id
    def to_dict(self):
        return {
            'id' : self.id,
            'student_id': self.student_id,
            'faculty_id': self.faculty_id,
        }


#+END_SRC
**** AcceptedApplication
- =AcceptedApplication= table stores the information of the student and the corresponding subject which are accepted by the =TA-CHAIR= .
- It contain the following fields 1) =student_id= (This can be used to get student)  
                                  2) =faculty_id= (This can be used to get Faculty)
- The code for =AcceptedApplication= is
#+BEGIN_SRC python
class AcceptedApplication(db.Model):
    __tablename__= 'acceptedapplication'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))

    def __init__(self,student_id,faculty_id):
        self.student_id=student_id
        self.faculty_id=faculty_id
    def to_dict(self):
        return {
            'id' : self.id,
            'student_id': self.student_id,
            'faculty_id': self.faculty_id,
        }


#+END_SRC
**** FinalTA
- =finalTA= table stores the information about final TA who was allocated to particular course .
- This table gets filled when student accepts his or her own TA-SHIP offer after =TA-CHAIR= selected him .
- It contains the following fields 1) =student_id= (This can be used to query student)
                                   2) =faculty_id= (This can be used to query faculty)
- The code for =FinalTA= table is
#+BEGIN_SRC python
class FinalTA(db.Model):
    __tablename__= 'finalta'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    student_id=db.Column(db.Integer,db.ForeignKey('student.id'))
    faculty_id=db.Column(db.Integer,db.ForeignKey('faculty.id'))

    def __init__(self,student_id,faculty_id):
        self.student_id=student_id
        self.faculty_id=faculty_id

    def to_dict(self):
        return {
            'id' : self.id,
            'student_id': self.student_id,
            'faculty_id': self.faculty_id,
        }


#+END_SRC
**** Tachair
- =Tachair= model  defines tachair  in our web application .
- It has the following fields =name= (name of tachair) , =email= (unique) , =password= .
- There will be only one TA-CHAIR in web application .
- The constraints on the =email= is that every TA-CHAIR has unique email.
- The code for =Tachair= model is 
#+BEGIN_SRC python

class Tachair(db.Model):
    __tablename__ = 'tachair'
    id = db.Column(db.Integer , primary_key = True,autoincrement = True)
    name = db.Column(db.String(25))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self,name,email,password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'name': self.name,
            'email': self.email,

        }

    def __repr__(self):
        return "Tachair<%d> %s" % (self.id, self.name)



#+END_SRC
***** Functionality
- =TAchair= will select students for TA-SHIP among the students who got accepted by the faculty for that corresponding subject .
- There is no registration required for the =TACHAIR= .   
** Code Explanation
*** functinalities
- assume all routes start with http://127.0.0.1:8080 .
**** /student(=get= method)
- This route displays the =student_login= page along with link to =regester_page= .
- If the student is already logged in then this route will display the home_page of the student. =[get]method= .
**** /faculty(=get= method)
- This route displays the =faculty_login= page along with the link to =regester_page= .
- If the faculty is already logged in then this route will display the home_page of the faculty who is logged in. (=[get]= method)
**** /tachair(=get= method)
- This route displays the =tachair_login= page .
- If the tachair is already logged in then this route will display the home_page of the tachair .(=[get]= metod)
**** /
- displays the main page which has links to =student_login= page , =faculty_login= page , =tachair_login= page .
**** /student(=post= method)
- This route when called takes form values =email= and =password= .
- queries for email in the database. If not present returns error message .
- if password's hashes are equal then home_page will be displayed .
**** /student/logout (=post= method)
- Removes the user session(log-out) and returns to the home page.
**** /student/registerpage(=get= method)
- dispalys student registerpage.
**** /student/register (=post= method)
- This is used for the student registeration .
- Takes form values =name= , =email= , =password= , =cgpa= , =rollno= and checks for the constraints on each of them , if every constraint 
  satisfies then =student= is regestered and is redirected to his home page .  
**** /student/addpreference (=post= method)
- By this route =student= chooses his first three preferences of subjects for TA-SHIP .
**** /student/addfinalta (=post= method)
- By this method =Student= can accept his TASHIP if he got selected for any subject or can wait for any other higher preferences .
- Once he has selected he will be assigned as TA for that course .
**** /faculty (=post= method)
- By this faculty can =login= in to his account . 
**** /faculty/registerpage (=get= method)
- It renders =register_page= for faculty registeration .
**** /faculty/register (=post= method)
- =Faculty= can register using this route.
**** /faculty/logout (=post= method)
- =faculty= can logout from his account . 
**** /faculty/add (=post= method)
- =Faculty= can accept students for his course among applied applications .
**** /tachair (=post= method)
- =TACHAIR= can login to his account using this . 
**** /tachair/logout (=post= method)
- =tachair= can logout from his account . 
**** /tachair/acc (=post= method)
- By this route =TACHAIR= can select final students who can get TASHIP among the students selected by the professor. 
