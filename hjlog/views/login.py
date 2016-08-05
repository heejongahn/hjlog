from hjlog import lm
from flask import render_template, redirect, flash, url_for, request, session
from hjlog.models import User
from hjlog.forms import LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse

msg_invalid_user = '등록된 관리자가 아닙니다 :('
msg_login_success = '관리자님 환영합니다 :)'
msg_logout_success = '성공적으로 로그아웃 되었습니다 :)'

msg_invalid_user = '등록된 관리자가 아닙니다 :('
msg_login_success = '관리자님 환영합니다 :)'
msg_logout_success = '성공적으로 로그아웃 되었습니다 :)'

def register(app):
    @app.route('/login', methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated():
            return redirect(url_for('about'))

        if 'next_url' not in session:
            session['next_url'] = urlparse(request.referrer).path

        form = LoginForm()
        if request.method == 'POST' and form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()

            if user and user.is_correct_password(form.password.data):
                login_user(user)
                flash(msg_login_success, 'success')
                session.pop('next_url', None)
                return form.redirect(url_for('about'))
            else:
                flash(msg_invalid_user, 'error')
                return redirect(url_for('login'))

        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        form = LoginForm()
        logout_user()
        flash(msg_logout_success, 'success')
        return form.redirect(url_for('about'))

    ####################
    # Helper functions #
    ####################
    @lm.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
