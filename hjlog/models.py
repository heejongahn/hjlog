from hjlog import db, bcrypt
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)

# Tag helper table
tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    category = db.Column(db.String(20))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag', secondary=tags,
        backref=db.backref('describes', lazy='dynamic'))
    comments = db.relationship('Comment', backref='original')
    photos = db.relationship('Photo', backref='original')

    def __init__(self, title, body, category, author, tags):
        self.title = title
        self.body = body
        self.category = category
        self.author = author
        self.tags = tags
        self.datetime = datetime.now()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag_name = db.Column(db.String(30), unique = True)

    def __init__(self, tag_name):
        self.tag_name = tag_name

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
    original_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, title, description, filename, original_id):
        self.title = title
        self.description = description
        self.filename = filename
        self.datetime = datetime.now()
        self.original_id = original_id
