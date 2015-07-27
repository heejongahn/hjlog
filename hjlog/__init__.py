from flask import Flask
from flask.ext.markdown import Markdown
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
Markdown(app)

db = SQLAlchemy(app)

from hjlog import views, models, forms
