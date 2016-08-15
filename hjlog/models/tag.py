from hjlog import db


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(30), unique=True)

    def __init__(self, tag_name):
        self.tag_name = tag_name
