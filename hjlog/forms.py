from flask_wtf import Form
from wtforms import TextField, TextAreaField, StringField, FileField, SelectField, PasswordField
from wtforms.validators import InputRequired, Length

class LoginForm(Form):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class PostForm(Form):
    title = StringField('제목', validators = [InputRequired(), Length(max=120)])
    body = TextAreaField('내용', validators = [InputRequired()])
    tags = StringField('글갈피', validators= [Length(max=100)])
    category = SelectField('분류', choices = [('daily', 'Daily'), ('study', 'Study')])
