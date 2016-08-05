# coding:utf-8
from flask_script import Manager, Shell
from app import create_app, db
from app.models import User, Category, Post, Comment, Page, Site, FriendLink
from flask_migrate import Migrate, MigrateCommand, upgrade

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Post=Post, User=User, Category=Category, \
                Comment=Comment, Page=Page, Site=Site, FriendLink=FriendLink)


manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    db.drop_all()
    db.create_all()

    user = User(name=u"admin", email="your email")
    user.password = "your password"
    default = Category(name=u"默认")
    db.session.add(user)
    db.session.add(default)
    db.session.commit()



if __name__ == '__main__':
    manager.run()
