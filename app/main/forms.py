from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email


# FORMS


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    header = StringField("Заголовок поста", validators=[DataRequired()])
    text = TextAreaField("Ваш текст", validators=[DataRequired()])
    photo = FileField("Загрузить обложку поста", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")
