import os
basedir = os.path.abspath(os.path.dirname(__file__))

# Form
SECRET_KEY = 'I cannot forget may eighth'
UPLOAD_FOLDER = 'hjlog/static/image'
ALLOWED_EXTENSIONS = set(['gif', 'jpg', 'jpeg', 'png'])

# SQLAlchemy
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'hjlog.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
