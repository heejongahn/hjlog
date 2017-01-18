from flask_wtf import Form
from wtforms import TextAreaField, StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, Optional, Length


class PostForm(Form):
    title = StringField('제목', validators=[InputRequired(), Length(max=120)])
    body = TextAreaField('내용', validators=[InputRequired()])
    private = BooleanField('비공개 설정', default=True)
    tags = StringField('글갈피', validators=[Length(max=100)])
    category = SelectField(
            '분류',
            validators=[Optional()],
            choices=[
                ('everyday', 'EVERYDAY'),
                ('study', 'STUDY'),
                ('idea', 'IDEA'),
                ('world', 'WORLD'),
                ('review', 'REVIEW'),
                ])
