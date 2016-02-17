from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_webpack import Webpack

app = Flask(__name__)
app.config.from_object('config')
try:
    app.config.from_envvar('RUN_OPT')
except:
    pass

webpack = Webpack()
webpack.init_app(app)

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
