from flask import render_template
from app.models import *
from app.main import main
from app.blueprints.auth import *

@main.route('/dashboard')
@is_logged_in
def index():
    tcount = db.engine.execute(f"SELECT count('T_ID') from TRAINERS").scalar()
    mcount = db.engine.execute(f"SELECT count('M_ID') from MEMBERS").scalar()
    excount = db.engine.execute(f"SELECT count('E_ID') from EXERCISE").scalar()
    eqcount = db.engine.execute(f"SELECT count('EQ_ID') from EQUIPMENTS").scalar()
    pcount = db.engine.execute(f"SELECT count('P_ID') from PACKAGE").scalar()
    topMembers = db.session.execute('SELECT * FROM members order by M_JOINDATE DESC limit 5')
    top_members = [row for row in topMembers]
    
    context={
        'title' : "Dashboard" ,
        'icon' : "glyphicon-cog",
        'isactive' : "active" ,
        'tcount' : tcount ,
        'mcount' : mcount ,
        'excount' : excount ,
        'eqcount' : eqcount ,
        'pcount' : pcount ,
        'top_members' : top_members
    }

    return render_template('/Dashboard/index.html', **context)

@main.route('/')
@main.route('/home')
def home():
    
    DisplayPackages = db.session.execute('SELECT * FROM package limit 4')
    display_packages = [row for row in DisplayPackages]
    
    DisplayEquipments = db.session.execute('SELECT * FROM equipments limit 4')
    display_equipments = [row for row in DisplayEquipments]
    eqp=[tup[1] for tup in display_equipments  ]
    eqp_images = ['back.jpg' , 'bicep.jpg' , 'shoulder.jfif' , 'tricep.jpg']
    
    eqp_tuples = tuple(zip(eqp , eqp_images))
  
    
    DisplayTrainers = db.session.execute('SELECT * FROM trainers limit 4')
    display_trainers = [row for row in DisplayTrainers]
    
    trainers=[tup[1] for tup in display_trainers ]
    trainer_images = ['4.jpg' , '3.jpg' , '2.jpg' , '1.jpg']
    
    trainer_tuples = tuple(zip(trainers , trainer_images))

    context = {
        'title': "TGYM" ,
        'display_packages' : display_packages ,
        'eqp_tuples' : eqp_tuples,
        'trainer_tuples' : trainer_tuples
    }
    
    return render_template('home.html' ,  **context)

@main.route('/login')
def dashboard():
    #db.create_all()
    return render_template('/Dashboard/login.html')

@main.route('/signin')
def dashboard_signin():
    #db.create_all()
    return render_template('/Dashboard/signin.html')

@main.route('/admin')
def admin_login():
    return render_template('/Dashboard/login.html' , isadmin=True)

@main.route('/profile')
@is_logged_in
def profile():
    #db.create_all()
    context = None
    if(session['gid'][0]=='T'):
        data=TRAINERS.query.filter(TRAINERS.T_GID==(session['gid'])).first()    
        context = {
            'gid' : data.T_GID,
            'name' : data.T_NAME,
            'gender' : data.T_GENDER,
            'email' : data.T_EMAIL,
            'mob' : data.T_MOB_NO,
            'doj' : data.T_JOINDATE,
            'location' : data.T_LOCATION
        }
    if(session['gid'][0]=='M'):
        data=MEMBERS.query.filter(MEMBERS.M_GID==(session['gid'])).first()
        context = {
            'gid' : data.M_GID,
            'name' : data.M_NAME,
            'gender' : data.M_GENDER,
            'dob' : data.M_DOB,
            'weight' : data.M_WEIGHT,
            'height' : data.M_HEIGHT,
            'email' : data.M_EMAIL,
            'mob' : data.M_MOB_NO,
            'doj' : data.M_JOINDATE,
            'location' : data.M_LOCATION,
            'tr_id' : data.TR_ID,
            'pk_id' : data.PK_ID  
        }
        
    return render_template('/Profile/index.html' , title="Profile" , **context)

