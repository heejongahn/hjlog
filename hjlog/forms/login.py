from urllib.parse import urlparse, urljoin

from flask import request, url_for, redirect, session
from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import InputRequired


class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='about', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class LoginForm(RedirectForm):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


####################
# helper functions #
####################


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def get_redirect_target():
    if 'next_url' in session:
        target = session['next_url']
    else:
        target = request.referrer
    if is_safe_url(target):
        return target
