import os
basedir = os.path.abspath(os.path.dirname(__file__))

BCRYPT_LOG_ROUNDS = 12

# Form
with open('SECRET_KEY') as secret_key:
    SECRET_KEY = secret_key.read().strip()

UPLOAD_FOLDER = 'hjlog/static/image/photo'
ALLOWED_EXTENSIONS = set(['gif', 'jpg', 'jpeg', 'png'])

# SQLAlchemy
if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('postgresql://hjlog:hjlog@localhost:5432/hjlog')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True

# MAX file upload size
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Webpack
WEBPACK_MANIFEST_PATH = os.path.join(basedir, 'manifest.json')
