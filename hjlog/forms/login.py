from flask_wtf import Form
from wtforms import TextField, PasswordField, HiddenField
from wtforms.validators import InputRequired
from urllib.parse import urlparse, urljoin, unquote
from flask import request, url_for, redirect, session


class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target()

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
    for target in request.args.get("next"), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return unquote(target or '')
