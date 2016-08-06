# coding:utf-8

import time
import datetime
import markdown
import collections
from flask import Flask, render_template, request, redirect, url_for, flash, g, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func  
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from forms import AddCommentForm
from .. import db
from . import main
from ..models import User, Post, Category, Comment, Page


@main.route('/')
@main.route('/index/<page>')
def index(page=1):
    pagination = Post.query.order_by("-pub_date").paginate(int(page), 10)
    posts = pagination.items
    return render_template("index.html", posts=posts, pagination=pagination, title=u"首页")


@main.route('/categorys')
def categorys():
    categorys = Category.query.all()
    return render_template("categorys.html", categorys=categorys, title=u"分类")


@main.route('/categorys/<name>')
def category(name):
    category = Category.query.filter(Category.name == name).first()
    posts = category.posts
    return render_template("category.html", posts=posts, title=name)


@main.route("/post/<title>", methods=['GET', 'POST'])
def post(title):
    post = Post.query.filter(Post.title == title).first()
    form = AddCommentForm()
    if form.validate_on_submit():
        comment = Comment(author_name=form.author_name.data, email=form.email.data,
                          content=form.content.data, post=post, pub_date=datetime.datetime.now())
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for("main.post", title=title))
    return render_template('post.html', post=post, form=form, title=title)


@main.route('/pages/<title>')
def pages(title):
    page = Page.query.filter_by(title=title).first()
    print dir(page)
    return render_template('page.html', page=page, title=title)


@main.route('/sitemap.xml', methods=['GET'])
def sitemap():
    url_list = []

    url_list.append(dict(
        loc=url_for('.index', _external=True),  # 生成绝对地址
        lastmod=datetime.date.today(),
        changefreq='weekly',
        priority=1,
    ))

    categories = Category.query.all()

    for category in categories:
        url_list.append(dict(
            loc=url_for('.category', name=category.name,  _external=True),
            changefreq='weekly',
            priority=0.8,
        ))

    posts = Post.query.all()

    for post in posts:
        url_list.append(dict(
            loc=url_for('.post', title=post.title, _external=True),
            lastmod=post.edit_date,
            changefreq='monthly',
            priority=0.6,
        ))

    sitemap_xml = render_template('sitemap.xml', url_list=url_list)
    res = make_response(sitemap_xml)
    res.mimetype = 'application/xml'
    return res


@main.route('/archives')
def archives():
    posts = Post.query.order_by("-pub_date")
    results = collections.OrderedDict()
    for i in posts:
        year_month = i.pub_date.strftime("%Y-%m")
        if year_month not in results:
            results[year_month] = []
        results[year_month].append(i)

    return render_template("archives.html", archives=results)