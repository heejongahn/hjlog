from hjlog import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    body = db.Column(db.Text)
    datetime = db.Column(db.DateTime)

    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.datetime = datetime.now()
