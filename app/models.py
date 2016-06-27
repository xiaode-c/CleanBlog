# coding:utf-8
from datetime import datetime
import markdown
from flask import Markup
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Page(db.Model):
    __tablename__="pages"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    md_text = db.Column(db.Text)
    html_text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())

    @classmethod
    def add(cls, title, md_text):
        now = datetime.now()
        html_text = markdown.markdown(md_text, extensions=[ \
                                    'markdown.extensions.fenced_code', \
                                    'markdown.extensions.codehilite'])
        page = cls(title=title, md_text=md_text, html_text=html_text, pub_date=now)
        db.session.add(page)
        db.session.commit()


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    content = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.now())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    disabled = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<comment: %r>' % self.content


    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        from faker import Factory
        fake = Factory.create()
        seed()
        post_count = Post.query.count()
        for i in range(count):
            p = Post.query.offset(randint(0, post_count-1)).first()
            comment = Comment(author_name=fake.name(),
                        email=fake.email(),
                        content=fake.text(),
                        pub_date=fake.date_time(),
                        post_id=p.id
                        )
            db.session.add(comment)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()



class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    md_text = db.Column(db.Text)
    html_text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, default=datetime.utcnow())
    edit_date = db.Column(db.DateTime, default=datetime.utcnow())
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship("Comment",  backref='post')

    @classmethod
    def add(cls, title, md_text, category_id, author_id):
        now = datetime.now()
        html_text = markdown.markdown(md_text, extensions=[ \
                                    'markdown.extensions.fenced_code', \
                                    'markdown.extensions.codehilite'])
        post = cls(title=title, md_text=md_text, html_text=html_text,\
                     category_id=category_id, author_id=author_id, \
                     pub_date=now, edit_date=now)
        db.session.add(post)
        db.session.commit()

    def html(self):
        html = markdown.markdown(self.md_text, extensions=[ \
                                'markdown.extensions.fenced_code', \
                                'markdown.extensions.codehilite'])
        return Markup(html)

    def __repr__(self):
        return '<Post: %r>' % self.title

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        from faker import Factory
        fake = Factory.create()
        seed()
        user_count = User.query.count()
        category_count = Category.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count-1)).first()
            c = Category.query.offset(randint(0, category_count-1)).first()
            post = Post(title=fake.word(),
                        md_text=fake.paragraph(),
                        html_text=fake.paragraph(),
                        pub_date=fake.date_time(),
                        category_id=c.id,
                        author_id=u.id
                        )
            db.session.add(post)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    posts = db.relationship('Post', backref='category', lazy='dynamic')

    def __repr__(self):
        return '<category name %r>' % self.name

    @staticmethod
    def generate_fake(count=50):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        from faker import Factory
        fake = Factory.create()
        seed()
        for i in range(count):
            category = Category(name=fake.word())
            db.session.add(category)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    email = db.Column(db.String(120), unique=True, index=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=86400):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


    #下面是Flask-Login需要的方法
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    #User类中自动添加的id
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.name

class Site(db.Model):
    __tablename__ = 'sites'
    id = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String(200))
    owner_name = db.Column(db.String(200))
    copyright = db.Column(db.String(200))
    friend_links = db.relationship('FriendLink', backref='sites', lazy='dynamic')

class FriendLink(db.Model):
    __tablename__ = 'friend_links'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    desc = db.Column(db.Text)
    link = db.Column(db.String(200))
    site = db.Column(db.Integer, db.ForeignKey('sites.id'))


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)
