from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms import ValidationError


# FORMS


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    category = SelectField('Выберите категорию', choices=[('space', 'Космос'), ('auto', 'Авто'), ('nature', 'Природа')])
    header = StringField("Заголовок поста", validators=[DataRequired()])
    text = TextAreaField("Ваш текст", validators=[DataRequired()])
    photo = FileField("Загрузить обложку поста", validators=[DataRequired()])
    submit = SubmitField("Подтвердить")

    def validate_photo(self, field):
        a = field.data.filename.split('.')
        if a[1] not in ['png','jpg','jpeg']:
            raise ValidationError("Формат изображения .jpg и .png")