from flask_wtf import Form
from wtforms import TextAreaField, StringField, FileField, SelectField
from wtforms.validators import InputRequired, Length

class PostForm(Form):
    title = StringField('제목', validators = [InputRequired(), Length(max=30)])
    body = TextAreaField('내용', validators = [InputRequired()])
    tags = StringField('글갈피')
    category = SelectField('분류', choices = [('daily', 'Daily'), ('study', 'Study')])

class CommentForm(Form):
    name = StringField('누가', validators = [InputRequired(), Length(max=30)])
    body = TextAreaField('어떤', validators = [InputRequired()])

class PhotoForm(Form):
    title = StringField('제목', validators = [InputRequired(), Length(max=30)])
    description = TextAreaField('사진에 대한 설명')
    photo = FileField('사진 파일', validators = [InputRequired()])
