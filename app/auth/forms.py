# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email, Length


class LoginForm(Form):
    email = StringField(u'邮箱', validators=[Required(), Email(), Length(1, 64)])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u"记住")
    submit = SubmitField(u'登录')
