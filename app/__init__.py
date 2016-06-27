# coding:utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
# from flask.ext.themes2 import Themes
# from flask.ext.themes import setup_themes
from config import config

app = Flask(__name__)

db = SQLAlchemy()
login_manager = LoginManager()
# theme = Themes()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/person_blog'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.config['SECRET_KEY'] = "strong"
    # app.config['debug'] = True

    db.init_app(app)
    login_manager.init_app(app)
    # theme.init_themes(app, app_identifier="blog")
    # setup_themes(app)

    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from admin import admin as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(main_blueprint)

    return app
