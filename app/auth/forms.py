from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

# FORMS


class AuthForm(FlaskForm):
    login = StringField(
        "Ваш email", validators=[DataRequired(), Length(1, 64), Email()]
    )
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember_me = BooleanField("Оставаться авторизованным")
    submit = SubmitField("Подтвердить")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField(
        "Имя пользователя",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Имя может состоят только из латинских букв, "
                "чисел, точек и нижних подчеркиваний",
            ),
        ],
    )
    password = PasswordField(
        "Пароль",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Пароли должны совпадать."),
        ],
    )
    password2 = PasswordField("Подтвердить пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Такой email уже зарегистрирован")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Такое имя пользователя уже существует")
