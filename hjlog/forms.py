from flask_wtf import Form
from wtforms import TextAreaField, StringField
from wtforms.validators import InputRequired, Length

class PostForm(Form):
    title = StringField('추억 제목', validators = [InputRequired(), Length(max=30)])
    body = TextAreaField('추억 내용', validators = [InputRequired()])

class CommentForm(Form):
    name = StringField('누가', validators = [InputRequired(), Length(max=30)])
    body = TextAreaField('어떤', validators = [InputRequired()])
