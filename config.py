import os


basedir = os.path.abspath(os.path.dirname(__file__))

BCRYPT_LOG_ROUNDS = 12

S3_BASE_URL = 'https://s3.ap-northeast-2.amazonaws.com/hjlog-photos/'
S3_BUCKET_NAME = 'hjlog-photos'

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
