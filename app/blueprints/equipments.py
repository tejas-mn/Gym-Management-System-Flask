from flask import Blueprint,render_template
from flask import *
from app.models import *

equipments_blueprint=Blueprint('equipments',__name__)


@equipments_blueprint.route('/' , methods=['POST' , 'GET'])
@equipments_blueprint.route('/<int:page_num>' , methods=['POST' , 'GET'])
def equipment(page_num=1):
    count = db.engine.execute(f"SELECT count('EQ_ID') from EQUIPMENTS").scalar()

    used_by = db.session.execute("SELECT  MEMBERS.M_NAME ,EQUIPMENTS.EQ_NAME , USES.EQP_ID FROM USES INNER JOIN EQUIPMENTS ON USES.EQP_ID = EQUIPMENTS.EQ_ID INNER JOIN MEMBERS ON USES.MEM_ID = MEMBERS.M_ID")
    used_by_member_tuples = [row for row in used_by]
  

    Data_Paginate = EQUIPMENTS.query.filter_by().paginate(per_page=5,page=page_num  , error_out = False)
   
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form.get('tag')
        search = "%{}%".format(tag)
        employees = EQUIPMENTS.query.filter(EQUIPMENTS.EQ_NAME.like(search)).paginate(per_page=5, error_out=False)
        context={
            'icon':"glyphicon-stats" ,
            'eq_tuples ': used_by_member_tuples ,
            'isequipments':"active" ,
            'title ': "Equipments" ,
            'equipments ': EQUIPMENTS.query.all() ,
            'members ': MEMBERS.query.all() ,
            'Data_Paginate':employees ,
            'isact':"active" ,
            'eqcount':count 
        }
        return render_template('/Dashboard/equipments.html' , **context)
    context={
         'icon':"glyphicon-stats" ,
         'eq_tuples' : used_by_member_tuples ,
         'isequipments':"active" ,
         'title' : "Equipments" ,
         'equipments' : EQUIPMENTS.query.all() ,
         'members' : MEMBERS.query.all() ,
         'Data_Paginate':Data_Paginate ,
         'isact':"active" ,
         'eqcount':count 
    }
    return render_template('/Dashboard/equipments.html' ,**context)

@equipments_blueprint.route('/add_equipment' , methods=['POST'])
def add_equipment():
   Data_Paginate = EQUIPMENTS.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       eq_name = request.form.get("eq_name")
       eq_qty = request.form.get("eq_qty")
       eq_cost = request.form.get("eq_cost")
       
       try:
           package = db.engine.execute(f"INSERT INTO EQUIPMENTS(EQ_NAME , EQ_QTY ,EQ_COST) VALUES( '{eq_name}' ,'{eq_qty}' ,'{eq_cost}' ) ")
       except  Exception as e:
           db.session.rollback()
           flash("Equipment already exists" , "danger" )
           return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))
             
   flash("Equipment added successfully" , "success")
   return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))

@equipments_blueprint.route('/edit_equipment/<int:eq_id>' , methods=['POST'])
def edit_equipment(eq_id):
   Data_Paginate = EQUIPMENTS.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       eq_name = request.form.get("eq_name")
       eq_qty = request.form.get("eq_qty")
       eq_cost = request.form.get("eq_cost")

       try:
           package = db.engine.execute(f"Update EQUIPMENTS SET EQ_NAME='{eq_name}' , EQ_QTY= '{eq_qty}'  , EQ_COST='{eq_cost}'  where EQ_ID ='{eq_id}'")
       except  Exception as e:
           db.session.rollback()
           flash("Some error occured" , "danger" )
           return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))
             
   flash("Equipment updated successfully" , "success")
   return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))

@equipments_blueprint.route('/delete_equipment/<int:eq_id>' )
def delete_equipment(eq_id):
    Data_Paginate = EQUIPMENTS.query.filter_by().paginate(per_page=5)
    try:
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM EQUIPMENTS WHERE EQUIPMENTS.EQ_ID = {eq_id}")
        db.session.commit()
    except  Exception as e:
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))
       
    flash("Equipment deleted successfully" , "danger")
    return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))

@equipments_blueprint.route("/assign_equipment" , methods=['POST'])
def assign_equipment():
    Data_Paginate = EQUIPMENTS.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
        mem_id = request.form.get('mem_id')
        eq_id = request.form.get('eq_id')
        
    if mem_id=='' or eq_id=='':
        flash("Equipment / Member cannot be empty" , "danger")
        return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))

    try:
        #db.session.execute("pragma foreign_keys=on")
        assign = db.session.execute(f"INSERT INTO USES(MEM_ID , EQP_ID) VALUES( '{mem_id}' ,'{eq_id}' ) ")
        db.session.commit()
    except  Exception as e:
        db.session.rollback()
        flash("Equipment already exists" , "danger" )
        return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))
             
    flash("Equipment assigned to member successfully" , "success")
    return redirect(url_for('equipments.equipment',page_num=Data_Paginate.pages))
    