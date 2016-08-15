from hjlog import db


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    original_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __init__(self, filename, original_id):
        self.filename = filename
        self.original_id = original_id
