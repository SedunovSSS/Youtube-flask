from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib, datetime

admins = ['admin']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
UPLOAD_FOLDER = './static/uploads'

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    path = db.Column(db.String(150), nullable=False)
    dateR = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Users %r>' % self.id


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watches = db.Column(db.Integer, default=0)
    author = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
    description = db.Column(db.String(500), nullable=False)
>>>>>>> c2b0d05 (shit)
>>>>>>> ec40277 (shit)
>>>>>>> 28d0da3 (shit)
>>>>>>> 44c78db (govno)
    path = db.Column(db.String(150), nullable=False)
    preview_path = db.Column(db.String(150), nullable=False)
    dateR = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Posts %r>' % self.id


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    author = db.Column(db.String(150), nullable=False)
    text = db.Column(db.String(500), nullable=False)
    dateR = db.Column(db.DateTime, default=datetime.datetime.utcnow())

    def __repr__(self):
        return '<Comments %r>' % self.id

