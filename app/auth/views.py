# coding:utf-8

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from forms import LoginForm
from . import auth
from ..models import User


@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print "hello"
        if user is not None and user.verify_password(form.password.data):
            print "hello"
            login_user(user, form.remember_me.data)
            print "hello"
            return redirect(request.args.get('next') or url_for("admin.admin_index"))
            print "hello"
        flash('Invalid username or password')
    return render_template("admin/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
