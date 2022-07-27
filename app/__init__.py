from datetime import timedelta
from distutils.command.config import config
from flask import Flask
from app.models import db
from config import DevelopmentConfig

##################################--FLASK-SETUP--#########################################
def create_app():
    
    app=Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    db.init_app(app)
    db.app = app
    
    #app.secret_key="abc"
    # #app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///gymdb.db'
    # #app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:Mysql123@localhost/demo'
    # app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:Mysql123@localhost/testdb'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

    
    # UPLOAD_FOLDER = 'static/images'

    # app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

    # #app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    # #app.config['SESSION_COOKIE_SECURE'] = True
    
    # global COOKIE_TIME_OUT
    # app.config['COOKIE_TIME_OUT'] = 60*60*24*7 #7 days
    # #COOKIE_TIME_OUT = 60*5 #5 minutes


    #import blueprints
    from app.main import main as main_bp
    from app.blueprints.auth import auth_blueprint    
    from app.blueprints.trainers import trainers_blueprint
    from app.blueprints.members import members_blueprint
    from app.blueprints.packages import packages_blueprint
    from app.blueprints.equipments import equipments_blueprint
    from app.blueprints.exercises import exercises_blueprint
    
    

    #register blueprints
    app.register_blueprint(main_bp , url_prefix='/')
    app.register_blueprint(auth_blueprint , url_prefix = '/auth')
    app.register_blueprint(trainers_blueprint , url_prefix = '/trainers')
    app.register_blueprint(members_blueprint , url_prefix = '/members')
    app.register_blueprint(packages_blueprint , url_prefix = '/packages')
    app.register_blueprint(equipments_blueprint , url_prefix = '/equipments')
    app.register_blueprint(exercises_blueprint , url_prefix = '/exercises')

    return app