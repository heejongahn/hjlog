from hjlog import lm
from flask import render_template, redirect, flash, url_for, request
from hjlog.models import User
from hjlog.forms import LoginForm
from flask.ext.login import login_user, logout_user, current_user, login_required

def register(app):
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

    ####################
    # Helper functions #
    ####################
    @lm.user_loader
    def load_user(user_id):
        return User.query.get(user_id)
