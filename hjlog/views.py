from hjlog import app
from flask import render_template

@app.route('/')
def index():
    return "Hello, world!"
