# coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import Required, Email, Length, DataRequired


class AddPostForm(Form):
    title = StringField(u"标题", validators=[Required()])
    md_text = TextAreaField(u"正文", validators=[DataRequired()])
    category = SelectField(u"分类", validators=[Required()])
    submit = SubmitField(u"发布")


class AddPageForm(Form):
    title = StringField(u"标题", validators=[Required()])
    md_text = TextAreaField(u"正文", validators=[DataRequired()])
    submit = SubmitField(u"发布")
