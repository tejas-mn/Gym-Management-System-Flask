import shortuuid
from app.models import TRAINER_SPEC, TRAINERS, db
from flask import *
from app.blueprints.auth import *

trainers_blueprint=Blueprint('trainers',__name__)

@trainers_blueprint.route('/' , methods=['GET'  ,'POST'])
@trainers_blueprint.route('/<int:page_num>' ,  methods=['GET' ,'POST'])
@is_logged_in
def trainer(page_num=1):
    #db.create_all()
    count = db.engine.execute(f"SELECT count('T_ID') from TRAINERS").scalar()

    exercises_conducted = db.session.execute("SELECT EXERCISE.E_NAME , TRAINERS.T_NAME , CONDUCTS.TR_ID FROM CONDUCTS INNER JOIN EXERCISE ON CONDUCTS.EX_ID=EXERCISE.E_ID INNER JOIN TRAINERS ON TRAINERS.T_ID=CONDUCTS.TR_ID")
    exercises_conducted_tuples = [row for row in exercises_conducted]

    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form.get('tag')
        search = "%{}%".format(tag)
        employees = TRAINERS.query.filter(TRAINERS.T_NAME.like(search)).paginate(per_page=5, error_out=False)
        context={
            'ex_tuples' : exercises_conducted_tuples ,
            'istrainers' : "active" ,
            'title' : "Trainers" ,
            'rows' : TRAINERS.query.all() ,
            'Data_Paginate' : employees ,
            'isact' : "active" ,
            'tcount' : count ,
            'specs' : TRAINER_SPEC.query.all()
        }
        return render_template('/Dashboard/trainers.html' , **context)

    Data_Paginate = TRAINERS.query.filter_by().paginate(per_page=5,page=page_num , error_out = False)
    context={
        'ex_tuples' : exercises_conducted_tuples ,
        'istrainers' : "active" ,
        'title' : "Trainers" ,
        'icon' : "glyphicon-user" ,
        'rows' :  TRAINERS.query.all() ,
        'Data_Paginate' : Data_Paginate ,
        'isact' : "active" ,
        'tcount' : count ,
        'specs'  :  TRAINER_SPEC.query.all()
    }
    return render_template('/Dashboard/trainers.html' , **context)


@trainers_blueprint.route('/add_trainer' , methods=['POST'])
@is_logged_in
def add_trainer():
   Data_Paginate = TRAINERS.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       t_name = request.form.get("t_name")
       t_gender = request.form.get("t_gender")
       #t_joindate = datetime.utcnow().date()
       t_email = request.form.get("t_email")
       t_mob_no = request.form.get("t_mob_no")
       t_location = request.form.get("t_location")
       t_joindate = request.form.get("t_joindate")
       t_gid = 'T' + shortuuid.ShortUUID().random(length=7)
       
       try:
           trainer = db.engine.execute(f"INSERT INTO TRAINERS(T_NAME , T_GENDER,T_JOINDATE ,T_EMAIL ,T_MOB_NO , T_LOCATION , T_GID) VALUES( '{t_name}' ,'{t_gender}' ,'{t_joindate}' ,'{t_email}' , '{t_mob_no}' , '{t_location}' , '{t_gid}') ")
           #gid = db.engine.execute(f"INSERT INTO USER_DATA(U_GID) VALUES('{t_gid}')") 
       except  Exception as e:
           db.session.rollback()
           flash("Trainer / email / mobile number already exists" , "danger" )
           return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

   flash("Trainer added successfully" , "success")
   return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

@trainers_blueprint.route('/add_spec' , methods=['POST'])
@is_logged_in
def add_spec():
    Data_Paginate = TRAINERS.query.filter_by().paginate(per_page=5)
    if request.method == "POST":
        t_id = request.form.get("t_id")
        t_spec = request.form.get("t_spec")
    try:
        trainer_spec = db.engine.execute(f"INSERT INTO TRAINER_SPEC(T_SPEC , TR_ID ) VALUES( '{t_spec}' ,'{t_id}' ) ")
    except  Exception as e:
        db.session.rollback()
        flash("Trainer / Specialization already exists" , "danger" )
        return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

    flash("Trainer specialization added successfully" , "success")
    return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))


@trainers_blueprint.route('/edit_trainer/<int:t_id>' ,methods=["POST"])
@is_logged_in
def edit_trainer(t_id):
    Data_Paginate = TRAINERS.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
        t_name = request.form.get("t_name")
        t_gender = request.form.get("t_gender")
        t_email = request.form.get("t_email")
        t_mob_no = request.form.get("t_mob_no")
        t_location = request.form.get("t_location")
        t_joindate = request.form.get("t_joindate")

        try:
            db.engine.execute(f"Update  TRAINERS SET T_NAME='{t_name}' , T_GENDER= '{t_gender}'  , T_EMAIL='{t_email}' ,T_MOB_NO=  '{t_mob_no}'  , T_LOCATION='{t_location}' , T_JOINDATE = '{t_joindate}' where T_ID ='{t_id}' ")
            flash("Trainer updated successfully" , "success")
        except  Exception as e:
    
            db.session.rollback()
            flash("Some error occured" , "danger" )
            return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

    return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

@trainers_blueprint.route('/delete_trainer/<int:t_id>' )
@is_logged_in
def delete_trainer(t_id):
    Data_Paginate = TRAINERS.query.filter_by().paginate(per_page=5)
    try:
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM TRAINERS WHERE TRAINERS.T_ID = {t_id}")
        db.session.commit()
    except  Exception as e:
    
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))

    flash("Trainer deleted successfully" , "danger")
    return redirect(url_for('trainers.trainer',page_num=Data_Paginate.pages))
