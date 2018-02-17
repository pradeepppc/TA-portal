from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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





