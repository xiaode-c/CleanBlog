import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # DEBUG = True
    DUOSUO_SHORT_NAME = os.environ.get('DUOSHUO_SHORT_NAME')　　# 多说评论设置，如果不设置，默认是自带的评论
    CNZZ_CONFIG = True  # 这里是设置CNZZ统计，可以关闭，或者在layout.html中设置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'mysql://root:123456@localhost/person_blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SERVER_NAME = 'localhost:5000'
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    WTF_CSRF_ENABLED = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
