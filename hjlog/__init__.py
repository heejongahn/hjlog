from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
try:
    app.config.from_envvar('RUN_OPT')
except:
    app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

bcrypt = Bcrypt(app)
CsrfProtect(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

from hjlog.views import init_app as init_view; init_view(app)
