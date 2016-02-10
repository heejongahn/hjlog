from hjlog import db
from datetime import datetime

# Tag helper table
tags = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)
    category = db.Column(db.String(20))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship(
        'Tag',
        secondary=tags,
        backref=db.backref('describes', lazy='dynamic'))
    photos = db.relationship('Photo', backref='original')

    def __init__(self, title, body, category, author, tags):
        self.title = title
        self.body = body
        self.category = category
        self.author = author
        self.tags = tags
        self.datetime = datetime.now()
