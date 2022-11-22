from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String(50))
    username = db.Column(db.String(50))
    email = db.Column(db.String(50),unique=True)
    phonenumber = db.Column(db.String(20))
    password = db.Column(db.String(50))
    dogs = db.relationship('Dog')

class Dog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dogname = db.Column(db.String(50))
    dogbreed = db.Column(db.String(50))
    dogage = db.Column(db.Integer)
    dogpincode = db.Column(db.String(20))
    dogcity = db.Column(db.String(20))
    dogdescription = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    dogownerid = db.Column(db.Integer, db.ForeignKey('user.id'))




