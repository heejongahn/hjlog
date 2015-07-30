from hjlog import app, db
from flask import render_template, redirect, request, url_for
from werkzeug import secure_filename
from sqlalchemy import desc
from .models import Post, Comment, Photo
from .forms import PostForm, CommentForm, PhotoForm
import os

# About
@app.route('/')
def index():
    return render_template('index.html')

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Blog
@app.route('/posts')
def posts():
    posts = Post.query.order_by(desc(Post.datetime)).all()
    return render_template('posts.html', posts = posts)

@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    form = CommentForm()
    post = Post.query.filter_by(id=id).one()
    comments = []
    try:
        comments = Comment.query.filter_by(original=post).all()
    except:
        pass

    if form.validate_on_submit():
        name, ip, body, o_id = (request.form.get('name'), request.remote_addr,
                request.form.get('body'), post.id)
        comment = Comment(name, ip, body, o_id)

        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('post', id=post.id, comments=comments, form=form))

    return render_template('post.html', post=post, comments=comments, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        title, body = request.form.get('title'), request.form.get('body')
        post = Post(title, body)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post', id=post.id))

    return render_template('post_new.html', form=form)

@app.route('/post/<id>/edit', methods=['GET', 'POST'])
def post_edit(id):
    post = Post.query.filter_by(id=id).one()
    form = PostForm(title = post.title, body = post.body)

    if form.validate_on_submit():
        title, body = request.form.get('title'), request.form.get('body')
        post.title, post.body = title, body

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post', id=post.id))

    return render_template('post_edit.html', form=form, id=post.id)

# Photo
@app.route('/photo')
def photo():
    photos = Photo.query.order_by(desc(Photo.datetime)).all()
    return render_template('photo.html', photos=photos)

@app.route('/photo/add', methods=['GET', 'POST'])
def photo_add():
    form = PhotoForm()
    if request.method == 'POST' and form.validate_on_submit:
        title, description = request.form.get('title'), request.form.get('description')
        uploaded_file = request.files['photo']
        print (uploaded_file.filename)

        if allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            flash("올바른 사진 파일이 아닙니다!!!", 'danger')
            return redirect(url_for('photo_add'))

        photo = Photo(title, description, filename)

        db.session.add(photo)
        db.session.commit()
        return redirect(url_for('photo'))

    return render_template('photo_add.html', form=form)
