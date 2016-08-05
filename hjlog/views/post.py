from hjlog import db

from flask import render_template, redirect, request, url_for, flash
from sqlalchemy import desc
from hjlog.models import Post, Photo, Tag
from hjlog.forms import PostForm
from flask.ext.login import current_user, login_required
import os

msg_invalid_category = '존재하지 않는 카테고리입니다!'
msg_invalid_input = '이런, 뭔가 빼먹으신 모양인데요?'
msg_delete_success = '성공적으로 삭제되었습니다 :)'

def register(app):
    @app.route('/posts/<category>', defaults={'page': 1})
    @app.route('/posts/<category>/<page>')
    def posts(category, page):
        if category not in ['everyday', 'idea', 'study', 'world']:
            flash(msg_invalid_category, 'warning')
            return redirect(url_for('posts', category='everyday'))

        pgn = Post.query.filter_by(category=category).order_by(desc(Post.datetime))\
            .paginate(int(page), per_page=10)
        return render_template('posts.html', posts=pgn.items, c=category, pgn=pgn)

    @app.route('/post/<id>')
    def post(id):
        post = Post.query.filter_by(id=id).one()
        category = post.category

        base = Post.query.filter_by(category=category)

        prv = base.order_by(desc("id")).filter(Post.id<id).first()
        nxt = base.order_by("id").filter(Post.id>id).first()

        return render_template('post.html', post=post, prv=prv, nxt=nxt)

    @app.route('/posts/<category>/new', methods=['GET', 'POST'])
    @login_required
    def post_new(category):
        if category not in ['everyday', 'idea', 'study', 'world']:
            flash(msg_invalid_category, 'warning')
            return redirect(url_for('post_new', category='everyday'))

        form = PostForm()

        if request.method == 'GET':
            return render_template('post_new.html', form=form, c=category)

        # Form Data Submitted
        if form.validate_on_submit():
            # Valid input
            title, body, category, author, tag_names = (
                request.form.get('title'), request.form.get('body'),
                category, current_user,
                request.form.get('tags'))
            tags = create_tags(tag_names)

            post = Post(title, body, category, author, tags)
            db.session.add(post)
            db.session.commit()

            photo_names = request.form.get('photonames')
            create_photos(photo_names, post)

            return redirect(url_for('post', id=post.id))

        # Invalid input
        flash(msg_invalid_input, 'warning')
        return render_template('post_new.html', form=form, c=category)

    @app.route('/post/<id>/edit', methods=['GET', 'POST'])
    @login_required
    def post_edit(id):
        post = Post.query.filter_by(id=id).one()

        tags_str = ", ".join([tag.tag_name for tag in post.tags])
        form = PostForm(title=post.title, body=post.body, tags=tags_str,
                        category=post.category)

        if request.method == 'GET':
            return render_template('post_edit.html', form=form, id=post.id)

        # Form Data Submitted
        if form.validate_on_submit():
            old_tags = post.tags

            # Valid input
            title, body, category, tag_names = (
                request.form.get('title'), request.form.get('body'),
                request.form.get('category'), request.form.get('tags'))
            tags = create_tags(tag_names)

            post.title, post.body, post.category, post.tags = title, body, category, tags
            db.session.add(post)
            db.session.commit()

            delete_orphan_tag(old_tags)

            photo_names = request.form.get('photonames')
            create_photos(photo_names, post)

            return redirect(url_for('post', id=post.id))

        # Invalid input
        flash(msg_invalid_input, 'warning')
        return render_template('post_write.html', form=form, id=post.id)

    @app.route('/post/<id>/delete')
    @login_required
    def post_delete(id):
        post = Post.query.filter_by(id=id).one()

        photos = Photo.query.filter_by(original_id=id).all()
        delete_photos(photos, app.config['UPLOAD_FOLDER'])

        tags = post.tags

        db.session.delete(post)
        db.session.commit()

        delete_orphan_tag(tags)

        flash(msg_delete_success, 'success')
        return redirect(url_for('posts', category='everyday'))

    @app.route('/search/<tag_name>', defaults={'page': 1})
    @app.route('/search/<tag_name>/<page>')
    def search(tag_name, page):
        pgn = Post.query.filter(Post.tags.any(tag_name=tag_name))\
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

        try:
            t = Tag(tag_name)
            db.session.add(t)
            db.session.commit()
        except:
            db.session.rollback()
            t = Tag.query.filter_by(tag_name=tag_name).one()
        finally:
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
