from flask import Flask
from flask.ext.markdown import Markdown

app = Flask(__name__)
Markdown(app)

from hjlog import views
