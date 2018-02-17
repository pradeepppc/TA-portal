from flask import *
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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



    
