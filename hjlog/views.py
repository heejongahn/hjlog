from hjlog import app, db
from flask import render_template, redirect, request, url_for
from .models import Post
from .forms import PostForm

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

@app.route('/write', methods=['GET', 'POST'])
def write():
    form = PostForm()
    if form.validate_on_submit():
        title, body = request.form.get('title'), request.form.get('body')
        post = Post(title, body)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('article', id=post.id))

    return render_template('write.html', form=form)
