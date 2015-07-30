from hjlog import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    comments = db.relationship('Comment', backref='original')

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    ip = db.Column(db.String(20))
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    original_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, name, ip, body, original_id):
        self.name = name
        self.ip = ip
        self.body = body
        self.datetime = datetime.now()
        self.original_id = original_id

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(30))
    description = db.Column(db.Text)
    filename = db.Column(db.String(100))
    datetime = db.Column(db.DateTime)

    def __init__(self, title, description, filename):
        self.title = title
        self.description = description
        self.filename = filename

        self.datetime = datetime.now()
