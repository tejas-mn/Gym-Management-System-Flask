from datetime import timedelta
import os 
basedir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
    #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gymdb.db'
    #app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:Mysql123@localhost/demo'
    #SECRET_KEY = os.environ.get('SECRET_KEY')
    SECRET_KEY = 'abc'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI= 'mysql://root:Mysql123@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    COOKIE_TIME_OUT = 60*60*24*7 #7 days
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
    

class TestingConfig(Config):
    DEBUG = False
    #SQLALCHEMY_DATABASE_URI= 'sqlite:///' + os.path.join(basedir , 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    COOKIE_TIME_OUT = 60*60*24*7 #7 days
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])
    

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI= 'mysql://root:Mysql123@localhost/testdb'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    COOKIE_TIME_OUT = 60*60*24*7 #7 days
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)
    UPLOAD_FOLDER = 'static/images'
    ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])