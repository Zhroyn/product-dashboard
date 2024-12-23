from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from wtforms import StringField, PasswordField, EmailField, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    account = StringField(
        label='Account',
        validators=[
            DataRequired(message='必须包含账号'),
            Length(min=6, max=100, message='账号的长度必须在 6 到 100 个字符之间')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(message='必须包含密码'),
            Length(min=6, max=20, message='密码的长度必须在 6 到 20 个字符之间')
        ]
    )


class SignupForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            DataRequired(message='必须包含用户名'),
            Length(min=6, max=100, message='用户名的长度必须在 6 到 100 个字符之间')
        ]
    )
    email = EmailField(
        label='Email',
        validators=[
            DataRequired(message='必须包含邮箱'),
            Email(message='邮箱格式不正确'),
            Length(min=6, max=100, message='邮箱的长度必须在 6 到 100 个字符之间')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(message='必须包含密码'),
            Length(min=6, max=20, message='密码的长度必须在 6 到 20 个字符之间')
        ]
    )

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在')
