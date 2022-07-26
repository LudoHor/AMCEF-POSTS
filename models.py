from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from apiflask.fields import Integer, String, Field
from apiflask import APIFlask, Schema
from apiflask.validators import Range


basedir = os.path.abspath(os.path.dirname(__file__))

app = APIFlask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "AMCEF123wwww"

db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    pk_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)

    def __init__(self, id, userId, title, body):

        self.id = id
        self.userId = userId
        self.title = title
        self.body = body

    def to_json(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'title': self.title,
            'body': self.body
        }


class PostInSchema(Schema):
    id = Integer(required=True, validate=Range(min=1))
    userId = Integer(required=True, validate=Range(min=1))
    title = String(required=True)
    body = String(required=True)


class PostUpdateInSchema(Schema):
    title = String(required=True)
    body = String(required=True)


class PostOutSchema(Schema):
    id = Integer()
    userId = Integer()
    title = String()
    body = String()
