from flask import Blueprint,render_template
from flask import *
from app.models import *
import shortuuid
from app.blueprints.auth import *

members_blueprint=Blueprint('members',__name__)

@members_blueprint.route('/' , methods=['POST' , 'GET'])
@members_blueprint.route('/<int:page_num>' ,  methods=['POST' , 'GET'])
@is_logged_in
def member(page_num=1):
    count = db.engine.execute(f"SELECT count('M_ID') from MEMBERS").scalar()
    exercises_takenup_by_members = db.session.execute("SELECT EXERCISE.E_NAME , MEMBERS.M_NAME , TAKEUP.MEM_ID FROM TAKEUP INNER JOIN EXERCISE ON TAKEUP.EX_ID=EXERCISE.E_ID INNER JOIN MEMBERS ON TAKEUP.MEM_ID = MEMBERS.M_ID")
    exercises_takenup_by_member_tuples = [row for row in exercises_takenup_by_members]
    equipments_used_by_members = db.session.execute("SELECT EQUIPMENTS.EQ_NAME , MEMBERS.M_NAME , USES.MEM_ID FROM USES INNER JOIN EQUIPMENTS ON USES.EQP_ID = EQUIPMENTS.EQ_ID INNER JOIN MEMBERS ON USES.MEM_ID = MEMBERS.M_ID")
    equipments_used_by_members_tuples = [row for row in equipments_used_by_members]

    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form.get('tag')
        search = "%{}%".format(tag)
        employees = MEMBERS.query.filter(MEMBERS.M_NAME.like(search)).paginate(per_page=5, error_out=False)
        context={
            'ex_tuples' : exercises_takenup_by_member_tuples ,
            'eq_tuples' : equipments_used_by_members_tuples,
            'ismembers' : "active" ,
            'title' : "Members" ,
            'icon' : "glyphicon-user",
            'rows' : MEMBERS.query.all() ,
            'Data_Paginate' : employees ,
            'isact' : "active" ,
            'mcount' : count ,
            'packages' : PACKAGE.query.all() ,
            'trainers' : TRAINERS.query.all()
        }
        return render_template('/Dashboard/members.html' , **context)

    Data_Paginate = MEMBERS.query.filter_by().paginate(per_page=5,page=page_num , error_out = False)
    
    context = {
        'ex_tuples' : exercises_takenup_by_member_tuples ,
        'eq_tuples' : equipments_used_by_members_tuples,
        'ismembers': "active" ,
        'title' : "Members" ,
        'icon':"glyphicon-user" ,
        'rows' : MEMBERS.query.all() ,
        'Data_Paginate':Data_Paginate ,
        'isact':"active" ,
        'mcount':count ,
        'packages' : PACKAGE.query.all() ,
        'trainers' : TRAINERS.query.all()
    }
    
    return render_template('/Dashboard/members.html' , **context)


@members_blueprint.route('/add_member' , methods=['POST'])
@is_logged_in
def add_member():
   Data_Paginate = MEMBERS.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       m_name = request.form.get("m_name")
       m_gender = request.form.get("m_gender")
       #m_joindate = dt.utcnow().date()
       m_dob = request.form.get("m_dob")
       m_weight = request.form.get("m_weight")
       m_height = request.form.get("m_height")
       m_email = request.form.get("m_email")
       m_mob_no = request.form.get("m_mob_no")
       m_joindate = request.form.get("m_joindate")
       m_location = request.form.get("m_location")
       tr_id = request.form.get("tr_id")
       pk_id = request.form.get("pk_id")
       m_gid = 'M' + shortuuid.ShortUUID().random(length=7)     
              
       try:
           #fk_check = db.session.execute("pragma foreign_keys=on")
           
           if m_dob=='':
               flash("Please select date of birth" , "danger")
               return redirect(url_for('members.member',page_num=Data_Paginate.pages))
           elif tr_id == '' or pk_id == '' or (pk_id=='' and tr_id==''):
               flash("Please Select the Trainer / Package","danger")
               return redirect(url_for('members.member',page_num=Data_Paginate.pages))
           
           trainer = db.session.execute(f"INSERT INTO MEMBERS(M_NAME , M_GENDER ,M_DOB ,M_WEIGHT ,M_HEIGHT , M_EMAIL , M_MOB_NO , M_JOINDATE , M_LOCATION , TR_ID , PK_ID , M_GID) VALUES( '{m_name}' ,'{m_gender}' ,'{m_dob}' ,'{m_weight}' , '{m_height}' , '{m_email}'  , '{m_mob_no}'  , '{m_joindate}' , '{m_location}' , '{tr_id}' , '{pk_id}' , '{m_gid}')")
           #gid = db.engine.execute(f"INSERT INTO USER_DATA(U_GID) VALUES('{m_gid}')")
           db.session.commit()
       except  Exception as e:
           print(e)
           db.session.rollback()
           flash("Member / email / mobile number already exists" , "danger" )
           return redirect(url_for('members.member',page_num=Data_Paginate.pages))
  
   flash("Member added successfully" , "success")
   return redirect(url_for('members.member',page_num=Data_Paginate.pages))


@members_blueprint.route('/edit_member/<int:m_id>' ,methods=["POST"])
@is_logged_in
def edit_member(m_id):
    Data_Paginate = MEMBERS.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
       m_name = request.form.get("m_name")
       m_gender = request.form.get("m_gender")
       m_dob = request.form.get("m_dob")
       m_weight = request.form.get("m_weight")
       m_height = request.form.get("m_height")
       m_email = request.form.get("m_email")
       m_mob_no = request.form.get("m_mob_no")
       m_location = request.form.get("m_location")
       m_joindate = request.form.get("m_joindate")

       tr_id = request.form.get("tr_id")
       pk_id = request.form.get("pk_id")
    
    try:
        db.engine.execute(f"Update  MEMBERS SET M_NAME='{m_name}' , M_GENDER= '{m_gender}'  , M_DOB='{m_dob}'  , M_WEIGHT='{m_weight}' , M_HEIGHT='{m_height}' , M_MOB_NO = '{m_mob_no}' , M_EMAIL = '{m_email}'  , M_LOCATION = '{m_location}' , M_JOINDATE='{m_joindate}'  , PK_ID = '{pk_id}' , TR_ID = '{tr_id}' where M_ID ='{m_id}' ")
        flash("Member updated successfully" , "success")
    except  Exception as e:
   
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('members.member',page_num=Data_Paginate.pages))
               
   
    return redirect(url_for('members.member',page_num=Data_Paginate.pages))


@members_blueprint.route('/delete_member/<int:m_id>' )
@is_logged_in
def delete_member(m_id):
    Data_Paginate = MEMBERS.query.filter_by().paginate(per_page=5)
    try:
      
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM MEMBERS WHERE MEMBERS.M_ID = {m_id}")
        db.session.commit()
    except  Exception as e:
       
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('members.member',page_num=Data_Paginate.pages))
       
    flash("Member deleted successfully" , "danger")
    return redirect(url_for('members.member',page_num=Data_Paginate.pages))