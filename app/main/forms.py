# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import Required, Email, Length, DataRequired


class AddCommentForm(Form):
    author_name = StringField(u"昵称", validators=[Required()])
    email = StringField(u"邮箱", validators=[Required(), Email()])
    content = TextAreaField(u"评论", validators=[DataRequired()])
    submit = SubmitField(u"评论")
