from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
import os
import hashlib, datetime
# import socket

admins = ['admin'] # write Admins logins in list
HOST = '127.0.0.1'
PORT = 5000
# Run on local ip
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# HOST = (s.getsockname()[0])
# s.close()

DB_NAME = "sqlite:///database.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
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


class Videos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    watches = db.Column(db.Integer, default=0)
    author = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    t = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500), nullable=False)
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
