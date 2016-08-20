# coding:utf-8

import datetime
import markdown
from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from forms import AddPostForm, AddPageForm
from .. import db
from . import admin
from ..models import Post, Category, Comment, User, Page, Site

# # 添加文章
# def add_post(title, md_text, category_id, author_id):
#     now = datetime.datetime.now()
#     html_text = markdown.markdown(md_text, extensions=[ \
#                                 'markdown.extensions.fenced_code', \
#                                 'markdown.extensions.codehilite'])
#     post = cls(title=title, md_text=md_text, html_text=html_text,\
#                  category_id=category_id, author_id=author_id, pub_date=now,
#                     edit_date=now)
#     db.session.add(post)
#     db.session.commit()


@admin.route('/')
@login_required
def admin_index():
    post_num = Post.query.count()
    category_num = Category.query.count()
    comment_num = Comment.query.count()
    nums = [category_num, post_num, comment_num]
    return render_template("admin/admin.html", nums=nums)


@admin.route('/posts')
@login_required
def admin_posts():
    posts = Post.query.order_by("-pub_date").all()
    return render_template("admin/posts.html", posts=posts)


@admin.route('/categorys', methods=['GET', 'POST'])
@login_required
def admin_categorys():
    if request.method == "POST":
        print dir(request)
        category_name = request.form["category_name"]
        category = Category(name=category_name)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("admin.admin_categorys"))
    categorys = Category.query.order_by("name").all()
    return render_template("admin/categorys.html", categorys=categorys)


@admin.route('/comments')
@login_required
def admin_comments():
    comments = Comment.query.order_by("-pub_date").all()
    return render_template("admin/comments.html", comments=comments)


@admin.route("/posts/add-post", methods=['GET', 'POST'])
@login_required
def add_post():
    form = AddPostForm()
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    if request.method == "POST":
        Post.add(title=form.title.data, md_text=form.md_text.data,
                 category_id=form.category.data, author_id=current_user.id)
    return render_template("admin/add-post.html", categories=categories, form=form)


@admin.route("/posts/edit-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    form = AddPostForm()
    categories = Category.query.all()
    form.category.choices = [(c.id, c.name) for c in categories]
    post = Post.query.get_or_404(post_id)
    if request.method == "GET":
        form.title.data = post.title
        form.md_text.data = post.md_text
        form.category.data = post.category
        return render_template("admin/add-post.html", post=post, form=form, categories=categories)
    else:
        post.title = form.title.data
        md_text = form.md_text.data
        post.md_text = md_text
        post.edit_date = datetime.datetime.utcnow()
        post.category_id = form.category.data
        post.html_text = markdown.markdown(post.md_text, extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables'])
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("admin.admin_posts"))


@admin.route('/posts/<int:post_id>/delete', methods=['GET'])
@login_required
def delete_post(post_id):
    post = Post.query.filter(Post.id == post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("admin.admin_posts"))


@admin.route('/categorys/<int:category_id>/delete', methods=['GET'])
@login_required
def delete_category(category_id):
    category = Category.query.filter(Category.id == category_id).first()
    if category:
        db.session.delete(category)
        db.session.commit()
    return redirect(url_for("admin.admin_categorys"))


@admin.route('/comments/<int:comment_id>/delete', methods=['GET'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    if comment:
        db.session.delete(comment)
        db.session.commit()
    return redirect(url_for("admin.admin_comments"))


@admin.route('/comments/edit-comment/<int:comment_id>/', methods=['GET'])
@login_required
def edit_comment(comment_id):
    comment = Comment.query.filter(Comment.id == comment_id).first()
    if comment.disabled == False:
        comment.disabled = True
    else:
        comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    # return redirect(url_for("admin.admin_comments"))
    return redirect(url_for("admin.admin_comments"))


@admin.route('/pages')
@login_required
def admin_pages():
    pages = Page.query.all()
    return render_template("admin/pages.html", pages=pages)


@admin.route("/pages/add-page", methods=['GET', 'POST'])
@login_required
def add_page():
    form = AddPageForm()
    if request.method == "POST":
        Page.add(title=form.title.data, md_text=form.md_text.data)
    return render_template("admin/add-page.html", form=form)


@admin.route("/pages/edit-page/<int:page_id>", methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    form = AddPageForm()
    page = Page.query.get_or_404(page_id)
    if request.method == "GET":
        form.title.data = page.title
        form.md_text.data = page.md_text
        return render_template("admin/add-page.html", page=page, form=form)
    else:
        page.title = form.title.data
        page.md_text = form.md_text.data
        page.html_text = markdown.markdown(page.md_text, extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.codehilite',
            'markdown.extensions.tables'])
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("admin.admin_pages"))


@admin.route('/pages/<int:page_id>/delete', methods=['GET'])
@login_required
def delete_page(page_id):
    page = Page.query.filter(Page.id == page_id).first()
    if page:
        db.session.delete(page)
        db.session.commit()
    return redirect(url_for("admin.admin_pages"))


@admin.route('/settings', methods=["GET", "POST"])
@login_required
def set():
    site = Site.query.first()
    if request.method == "POST":
        sitename = request.form.get("sitename")
        ownername = request.form.get("ownername")
        copyright = request.form.get("copyright")
        print copyright, sitename, ownername
        site.sitename = sitename
        site.owner_name = ownername
        site.copyright = copyright
        db.session.add(site)
        db.session.commit()
        return redirect(url_for("admin.set"))
    form = {"sitename":site.sitename, "ownername":site.owner_name, "copyright":site.copyright}
    return render_template("admin/settings.html", form=form)
