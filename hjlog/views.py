from hjlog import app, db, lm
from flask import render_template, redirect, request, url_for, flash, jsonify
from werkzeug import secure_filename
from sqlalchemy import desc
from .models import Post, Photo, Tag, User
from .forms import PostForm, LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
import os
import time

# Login
@lm.user_loader
def load_user(user_id):
    u = None
    try:
        u = User.query.filter_by(id=user_id).one()
    except:
        pass

    return u

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('about'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            user = User.query.filter_by(username=form.username.data).first_or_404()
        except:
            flash('등록된 관리자가 아닙니다 :(', 'warning')
            return redirect(url_for('login'))

        if user.is_correct_password(form.password.data):
            login_user(user)
            flash('관리자님 환영합니다 :)', 'success')
            return redirect(url_for('about'))
        else:
            flash('올바르지 않은 ID/PW 쌍입니다 :-(', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('성공적으로 로그아웃 되었습니다 :)', 'success')

    return redirect(url_for('about'))

# 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', code=404), 404

# 405
@app.errorhandler(405)
def method_not_allowed(e):
    return render_template('error.html', code=405), 405

# 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', code=500), 500

# About
@app.route('/')
def about():
    return render_template('about.html')

@app.route('/.well-known/acme-challenge/<tmp>')
def letsencrpyt(tmp):
    with open('.well-known/acme-challenge/{}'.format(tmp)) as f:
        answer = f.readline().strip()

    return answer

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Blog
@app.route('/posts/<category>/<page>')
def posts(category, page):
    pgn = Post.query.filter_by(category=category).order_by(desc(Post.datetime))\
            .paginate(int(page), per_page = 10)
    return render_template('posts.html', posts = pgn.items, c = category, pgn = pgn)

@app.route('/post/<id>')
def post(id):
    post = Post.query.filter_by(id=id).one()
    return render_template('post.html', post=post)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if request.method=='POST':
        if form.validate_on_submit():
            title, body, category, author, tag_names = request.form.get('title'), request.form.get('body'), \
                    request.form.get('category'), current_user, request.form.get('tags')

            # Tagging
            tag_names = [tag_name.strip('\n').strip(' ') for tag_name in tag_names.split(',')]
            if tag_names == ['']:
                tag_names = []

            tags = []
            for tag_name in tag_names:
                try:
                    t = Tag(tag_name)
                    db.session.add(t)
                    db.session.commit()
                except:
                    db.session.rollback()
                    t = Tag.query.filter_by(tag_name = tag_name).one()
                finally:
                    tags.append(t)

            post = Post(title, body, category, author, tags)

            db.session.add(post)
            db.session.commit()

            # Photo
            photo_names = request.form.get('photonames')
            if photo_names:
                photo_names = [photo_name for photo_name in photo_names.strip(' ').split(' ')]
                for photo_name in photo_names:
                    p = Photo(photo_name, post.id)
                    db.session.add(p)
                db.session.commit()

            return redirect(url_for('post', id=post.id))
        else:
            flash('이런, 뭔가 빼먹으신 모양인데요?', 'warning')
            return render_template('post_new.html', form=form)

    return render_template('post_new.html', form=form)

@app.route('/post/<id>/delete')
@login_required
def post_delete(id):
    post = Post.query.filter_by(id=id).one()
    photos = Photo.query.filter_by(original_id=id).all()
    for photo in photos:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], photo.filename))
        db.session.delete(photo)
    db.session.delete(post)
    db.session.commit()
    flash('성공적으로 삭제되었습니다 :)', 'success')
    return redirect(url_for('posts', category='daily', page=1))

@app.route('/post/<id>/edit', methods=['GET', 'POST'])
@login_required
def post_edit(id):
    post = Post.query.filter_by(id=id).one()

    tags_str = ", ".join([tag.tag_name for tag in post.tags])

    form = PostForm(title = post.title, body = post.body, tags=tags_str,
            category=post.category)

    if request.method == 'POST':
        if form.validate_on_submit():
            title, body, category, tag_names = request.form.get('title'), request.form.get('body'), \
                    request.form.get('category'), request.form.get('tags')

            # Tagging
            tag_names = [tag_name.strip('\n').strip(' ') for tag_name in tag_names.split(',')]
            if tag_names == ['']:
                tag_names = []

            tags = []
            for tag_name in tag_names:
                try:
                    t = Tag(tag_name)
                    db.session.add(t)
                    db.session.commit()
                except:
                    db.session.rollback()
                    t = Tag.query.filter_by(tag_name = tag_name).one()
                finally:
                    tags.append(t)

            post.title, post.body, post.category, post.tags = title, body, category, tags

            db.session.add(post)
            db.session.commit()

            #Photo
            photo_names = request.form.get('photonames')
            photo_names = [photo_name for photo_name in photo_names.strip(' ').split(' ')]
            for photo_name in photo_names:
                p = Photo(photo_name, post.id)
                db.session.add(p)
            db.session.commit()

            return redirect(url_for('post', id=post.id))

        else:
            flash('이런, 뭔가 빼먹으신 모양인데요?', 'warning')
            return render_template('post_edit.html', form=form, id=post.id)

    return render_template('post_edit.html', form=form, id=post.id)

@app.route('/photoajax', methods=['POST'])
@login_required
def photo_ajax():
    if request.method == 'POST':
        photo = request.files['file']

        if photo and allowed_file(photo.filename):
            filename = secure_filename(str(time.time())+photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            url = url_for('static', filename='image/photo/'+filename)
            return jsonify(correct=True, name=filename, url=url)

        elif not allowed_file(photo.filename):
            return jsonify(correct=False)
