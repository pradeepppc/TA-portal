from flask_sqlalchemy import SQLAlchemy
from flask import *
from app.student.models import *
from app.faculty.models import *
from app import db

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

