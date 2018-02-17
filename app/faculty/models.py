from flask_sqlalchemy import SQLAlchemy
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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
        

