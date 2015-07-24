from hjlog import app, db
from flask import render_template, redirect
from .models import Post

# About
@app.route('/')
def index():
    return render_template('index.html')

# Blog
@app.route('/post')
def post():
    posts = Post.query.all()
    return render_template('post.html', posts = posts)

@app.route('/post/<id>')
def article(id):
    post = Post.query.filter_by(id=id).one()
    return render_template('article.html', post=post)
