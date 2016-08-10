from hjlog import db

from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import desc, or_
from hjlog.models import Post, Photo, Tag
from hjlog.forms import PostForm
from flask.ext.login import current_user, login_required
import os

MSG_INVALID_CATEGORY = '존재하지 않는 카테고리입니다!'
MSG_INVALID_INPUT = '이런, 뭔가 빼먹으신 모양인데요?'
MSG_DELETE_SUCCESS = '성공적으로 삭제되었습니다 :)'
MSG_UNAUTHORIZED = '이 글에 접근할 권한이 없습니다.'

ALLOWED_CATEGORIES = ['everyday', 'idea', 'study', 'world']

def register(app):
    @app.route('/posts/<category>', defaults={'page': 1})
    @app.route('/posts/<category>/<page>')
    def posts(category, page):
        if category not in ALLOWED_CATEGORIES:
            flash(MSG_INVALID_CATEGORY, 'warning')
            return redirect(url_for('posts', category='everyday'))

        pgn = get_visible_posts(current_user)\
                .filter_by(category=category)\
                .order_by(desc(Post.datetime))\
                .paginate(int(page), per_page=10)

        return render_template('posts.html', posts=pgn.items, c=category, pgn=pgn)

    @app.route('/post/<id>')
    def post(id):
        post = Post.query.get_or_404(id)

        if post.is_invisible_by(current_user):
            flash(MSG_UNAUTHORIZED, 'warning')
            return redirect(url_for('about'))

        base = get_visible_posts(current_user).filter_by(category=post.category)

        prv = base.order_by(desc("id")).filter(Post.id<id).first()
        nxt = base.order_by("id").filter(Post.id>id).first()

        return render_template('post.html', post=post, prv=prv, nxt=nxt)

    @app.route('/posts/<category>/new', methods=['GET', 'POST'])
    @login_required
    def post_new(category):
        if category not in ALLOWED_CATEGORIES:
            flash(MSG_INVALID_CATEGORY, 'warning')
            return redirect(url_for('post_new', category='everyday'))

        form = PostForm()

        if request.method == 'GET':
            return render_template('post_new.html', form=form, c=category)

        if form.validate_on_submit():
            keys = ['title', 'body', 'private', 'tags']
            title, body, private, tag_names =\
                    [request.form.get(key) for key in keys]

            tags = create_tags(tag_names)
            private = bool(private)

            post = Post(title, body, category, current_user, private, tags)
            db.session.add(post)
            db.session.commit()

            photo_names = request.form.get('photonames')
            create_photos(photo_names, post)

            return redirect(url_for('post', id=post.id))

        flash(MSG_INVALID_INPUT, 'warning')
        return render_template('post_new.html', form=form, c=category)

    @app.route('/post/<id>/edit', methods=['GET', 'POST'])
    @login_required
    def post_edit(id):
        post = Post.query.get_or_404(id)

        if post.is_invisible_by(current_user):
            flash(MSG_UNAUTHORIZED, 'warning')
            return redirect(url_for('about'))

        tags_str = ", ".join([tag.tag_name for tag in post.tags])
        form = PostForm(title=post.title, body=post.body, private=post.private,
                tags=tags_str, category=post.category)

        if request.method == 'GET':
            return render_template('post_edit.html', form=form, id=post.id)

        if form.validate_on_submit():
            keys = ['title', 'body', 'category', 'private', 'tags']
            title, body, category, private, tag_names =\
                    [request.form.get(key) for key in keys]

            private = bool(private)
            tags = create_tags(tag_names)

            removed = [tag for tag in post.tags if tag not in tags]

            post.title, post.body, post.category, post.private, post.tags =\
                    title, body, category, private, tags
            db.session.add(post)
            db.session.commit()

            delete_orphan_tag(removed)

            photo_names = request.form.get('photonames')
            create_photos(photo_names, post)

            return redirect(url_for('post', id=post.id))

        flash(MSG_INVALID_INPUT, 'warning')
        return render_template('post_write.html', form=form, id=post.id)

    @app.route('/post/<id>/delete')
    @login_required
    def post_delete(id):
        post = Post.query.get_or_404(id)

        if post.is_invisible_by(current_user):
            flash(MSG_UNAUTHORIZED, 'warning')
            return redirect(url_for('about'))

        photos = Photo.query.filter_by(original_id=id).all()
        delete_photos(photos, app.config['UPLOAD_FOLDER'])

        tags = post.tags

        db.session.delete(post)
        db.session.commit()

        delete_orphan_tag(tags)

        flash(MSG_DELETE_SUCCESS, 'success')
        return redirect(url_for('posts', category='everyday'))

    @app.route('/search/<tag_name>', defaults={'page': 1})
    @app.route('/search/<tag_name>/<page>')
    def search(tag_name, page):
        pgn = get_visible_posts(current_user)\
                .filter(Post.tags.any(tag_name=tag_name))\
                .paginate(int(page), per_page=10)

        return render_template('search.html', posts=pgn.items, pgn=pgn,
                tag_name=tag_name)


####################
# Helper functions #
####################

def create_tags(tag_names):
    tag_names = [name.strip() for name in tag_names.split(',')]

    if tag_names == ['']:
        tag_names = []

    tags = []
    for tag_name in tag_names:
        if tag_name == "":
            continue

        t = Tag.query.filter_by(tag_name=tag_name).first()
        if not t:
            t = Tag(tag_name)
            db.session.add(t)
            db.session.commit()

        tags.append(t)

    return tags

def create_photos(photo_names, original):
    photo_names = [name for name in photo_names.strip().split()]

    for photo_name in photo_names:
        p = Photo(photo_name, original.id)
        db.session.add(p)

    db.session.commit()

def delete_photos(photos, upload_folder):
    for photo in photos:
        os.remove(os.path.join(upload_folder, photo.filename))
        db.session.delete(photo)

def delete_orphan_tag(tags):
    for tag in tags:
        if not tag.describes.all():
            db.session.delete(tag)
            db.session.commit()

def get_visible_posts(current_user):
    if current_user and current_user.is_authenticated():
        return Post.query.filter(or_(~Post.private, Post.author == current_user))
    else:
        return Post.query.filter_by(private=False)
