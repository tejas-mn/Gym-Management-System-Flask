from flask_sqlalchemy import SQLAlchemy

#from settings import create_app
#import settings
#app = create_app()
#db=SQLAlchemy(settings.app)

db = SQLAlchemy()

CONDUCTS = db.Table('CONDUCTS',
    db.Column('TR_ID' , db.Integer , db.ForeignKey('TRAINERS.T_ID' , ondelete='CASCADE') , primary_key = True ),
    db.Column('EX_ID' , db.Integer , db.ForeignKey('EXERCISE.E_ID' , ondelete='CASCADE')  , primary_key = True  )
)

class UserData(db.Model):
    U_ID = db.Column(db.Integer, primary_key=True)
    U_NAME = db.Column(db.String(45), nullable=False)
    U_EMAIL = db.Column(db.String(20) , nullable = False , unique = True)
    U_PSWD = db.Column(db.String(100) , nullable = False , unique = True)
    U_GID =  db.Column(db.String(10), nullable = False , unique=True)
    
    def __init__(self, username, email, password,gid):
            self.U_NAME = username
            self.U_EMAIL = email
            self.U_PSWD = password
            self.U_GID = gid
            
class TRAINERS(db.Model):

    T_ID = db.Column(db.Integer, primary_key=True)
    T_NAME = db.Column(db.String(45), nullable=False)
    T_GENDER = db.Column(db.CHAR)
    T_JOINDATE = db.Column(db.Date , nullable = False)
    T_EMAIL = db.Column(db.String(20) , nullable = False , unique = True)
    T_MOB_NO = db.Column(db.String(14) , nullable = False , unique = True)
    T_LOCATION = db.Column(db.String(15))
    T_GID =  db.Column(db.String(10), nullable = False , unique=True)

    T_SPEC = db.relationship('TRAINER_SPEC' , backref = 'TRAINERS' , lazy = True , passive_deletes="all")

    conducting = db.relationship('EXERCISE' ,  secondary = CONDUCTS, backref = 'conducts' , lazy=True)

    def __init__(self  ,  t_name , t_gender , t_joindate , t_email ,  t_mob_no , t_location , t_gid):
       
        self.T_NAME = t_name
        self.T_GENDER = t_gender
        self.T_JOINDATE = t_joindate
        self.T_EMAIL = t_email
        self.T_MOB_NO = t_mob_no
        self.T_LOCATION = t_location
        self.T_GID = t_gid

class TRAINER_SPEC(db.Model):

    T_SPEC = db.Column(db.String(15), primary_key=True)
    TR_ID = db.Column(db.Integer ,  db.ForeignKey('TRAINERS.T_ID' , ondelete = 'CASCADE') , primary_key = True)

    def __init__(self  , t_spec , tr_id):
        self.T_SPEC  = t_spec
        self.TR_ID = tr_id

CONSISTS = db.Table('CONSISTS',
    db.Column('PK_ID' , db.Integer , db.ForeignKey('PACKAGE.P_ID' , ondelete = 'CASCADE') , primary_key = True ),
    db.Column('EX_ID' , db.Integer , db.ForeignKey('EXERCISE.E_ID' , ondelete = 'CASCADE')  , primary_key = True )
)

class PACKAGE(db.Model):
    P_ID = db.Column(db.Integer , primary_key = True)
    P_NAME = db.Column(db.String(15) , nullable = False)
    P_PRICE = db.Column(db.Integer , nullable=False)
    P_DURATION = db.Column(db.Integer , nullable = False)

    consisting = db.relationship('EXERCISE' , secondary = CONSISTS, backref = 'consists' , lazy = True)

    def __init__(self ,p_name , p_price , p_duration):
       
        self.P_NAME = p_name
        self.P_PRICE = p_price
        self.P_DURATION = p_duration

class EXERCISE(db.Model):
    E_ID = db.Column(db.Integer , primary_key = True)
    E_NAME = db.Column(db.String(15) , nullable = False)
    E_TYPE = db.Column(db.String(15))
    E_TIMESLOT = db.Column(db.Time , nullable = False)

    def __init__(self , e_name , e_type , e_timeslot):
        self.E_NAME = e_name
        self.E_TYPE = e_type
        self.E_TIMESLOT = e_timeslot


USES = db.Table('USES',
    db.Column('MEM_ID' , db.Integer , db.ForeignKey('MEMBERS.M_ID' , ondelete = 'CASCADE') , primary_key = True ),
    db.Column('EQP_ID' , db.Integer , db.ForeignKey('EQUIPMENTS.EQ_ID' , ondelete = 'CASCADE')  , primary_key = True )
)

TAKEUP = db.Table('TAKEUP',
    db.Column('MEM_ID' , db.Integer , db.ForeignKey('MEMBERS.M_ID' , ondelete = 'CASCADE') , primary_key = True  ),
    db.Column('EX_ID' , db.Integer , db.ForeignKey('EXERCISE.E_ID', ondelete = 'CASCADE')  , primary_key = True )
)

class MEMBERS(db.Model):
    M_ID = db.Column(db.Integer , primary_key = True)
    M_NAME = db.Column(db.String(15) , nullable = False)
    M_GENDER = db.Column(db.CHAR)
    M_DOB = db.Column(db.Date , nullable = False)
    M_WEIGHT = db.Column(db.Float)
    M_HEIGHT = db.Column(db.Float)
    M_EMAIL = db.Column(db.String(20) , nullable = False , unique = True)
    M_MOB_NO = db.Column(db.String(14) , nullable = False , unique = True)
    M_JOINDATE = db.Column(db.Date , nullable = False)
    M_LOCATION = db.Column(db.String(15))
    M_GID =  db.Column(db.String(10), nullable = False , unique=True)

    TR_ID = db.Column(db.Integer ,  db.ForeignKey('TRAINERS.T_ID' , ondelete='SET NULL') )
    PK_ID = db.Column(db.Integer ,  db.ForeignKey('PACKAGE.P_ID' , ondelete='SET NULL') )

    using = db.relationship('EQUIPMENTS' , secondary = USES, backref = 'uses' , lazy = True)
    taking_up = db.relationship('EXERCISE' , secondary = TAKEUP , backref = 'takes_up' , lazy = True)

    def __init__(self , m_name , m_gender , m_dob , m_weight , m_height , m_email , m_mob_no, m_location , m_joindate , tr_id , pk_id , m_gid):
       
        self.M_NAME = m_name
        self.M_GENDER = m_gender
        self.M_DOB = m_dob
        self.M_WEIGHT = m_weight
        self.M_HEIGHT = m_height
        self.M_EMAIL = m_email
        self.M_MOB_NO = m_mob_no
        self.M_LOCATION = m_location
        self.M_JOINDATE = m_joindate
        self.M_GID = m_gid
        
        self.TR_ID = tr_id
        self.PK_ID = pk_id



class EQUIPMENTS(db.Model):
    EQ_ID = db.Column(db.Integer , primary_key = True)
    EQ_NAME = db.Column(db.String(15) , nullable = False)
    EQ_QTY = db.Column(db.Integer)
    EQ_COST = db.Column(db.Float)

    def __init__(self , eq_name , eq_qty , eq_cost ):
       
        self.EQ_NAME = eq_name
        self.EQ_QTY = eq_qty
        self.EQ_COST = eq_cost