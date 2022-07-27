from flask import Blueprint,render_template
from flask import *
from app.models import *

exercises_blueprint=Blueprint('exercises',__name__)

@exercises_blueprint.route('/'  , methods=['GET', 'POST'])
@exercises_blueprint.route('/<int:page_num>' , methods=['GET', 'POST'])
def exercise(page_num=1):
    count = db.engine.execute(f"SELECT count('E_ID') from EXERCISE").scalar()
    
    Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5,page=page_num , error_out = False)
   
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form.get('tag')
        search = "%{}%".format(tag)
        employees = EXERCISE.query.filter(EXERCISE.E_NAME.like(search)).paginate(per_page=5, error_out=False)
        context={
            'icon' : "glyphicon glyphicon-heart" ,
            'isexercises' : "active" ,
            'title' : "Exercises" ,
            'Data_Paginate' : employees,
            'tag' : tag ,
            'isact': "active" ,
            'excount' : count ,
            'rows' : EXERCISE.query.all() ,
            'packages'  : PACKAGE.query.all() ,
            'exercises' : EXERCISE.query.all() ,
            'trainers' : TRAINERS.query.all() ,
            'members' : MEMBERS.query.all()
        }
        return render_template('/Dashboard/exercises.html' , **context)
    context={
        'icon' : "glyphicon glyphicon-heart" ,
        'isexercises' : "active" ,
        'title' : "Exercises" ,
        'Data_Paginate' : Data_Paginate ,
        'isact' : "active" ,
        'excount' : count ,
        'rows' : EXERCISE.query.all() ,
        'packages'  : PACKAGE.query.all() ,
        'exercises' : EXERCISE.query.all() ,
        'trainers' : TRAINERS.query.all() ,
        'members' : MEMBERS.query.all()
    }   
    return render_template('/Dashboard/exercises.html' , **context)


@exercises_blueprint.route('/add_exercise' , methods=['POST'])
def add_exercise():
   Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       e_name = request.form.get("e_name")
       e_type = request.form.get("e_type")
       e_timeslot = request.form.get("e_timeslot")
       
       if e_name=='':
           flash("Please Enter the Exercise Name" , "danger")
           return redirect(url_for('exercises.exercise' , page_num = Data_Paginate.pages))
       
       if e_timeslot=='':
           flash("Please Enter the time Slot" , "danger")
           return redirect(url_for('exercises.exercise' , page_num = Data_Paginate.pages))

       try:
           exercise = db.session.execute(f"INSERT INTO EXERCISE(E_NAME , E_TYPE ,E_TIMESLOT) VALUES( '{e_name}' ,'{e_type}' ,'{e_timeslot}' ) ")
           db.session.commit()
       except  Exception as e:
           
           db.session.rollback()
           flash("Exercise already exists" , "danger" )
           return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
  
   flash("Exercise added successfully" , "success")
   return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))

@exercises_blueprint.route('/edit_exercise/<int:e_id>' , methods=['POST'])
def edit_exercise(e_id):
   Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       e_name = request.form.get("e_name")
       e_type = request.form.get("e_type")
       e_timeslot = request.form.get("e_timeslot")

       
       if e_name=='':
           flash("Please Enter the Exercise Name" , "danger")
           return redirect(url_for('exercises.exercise' , page_num = Data_Paginate.pages))
       
       if e_timeslot=='':
           flash("Please Enter the time Slot" , "danger")
           return redirect(url_for('exercises.exercise' , page_num = Data_Paginate.pages))
       
       try:
           exercise = db.engine.execute(f"Update EXERCISE SET E_NAME='{e_name}' , E_TYPE= '{e_type}'  , E_TIMESLOT='{e_timeslot}'  where E_ID ='{e_id}'")
          
       except  Exception as e:
          
           db.session.rollback()
           flash("Some error occured" , "danger" )
           return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
             
   flash("Exercise updated successfully" , "success")
   return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))


@exercises_blueprint.route('/delete_exercise/<int:e_id>' )
def delete_exercise(e_id):
    Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

    try:
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM EXERCISE WHERE EXERCISE.E_ID = {e_id}")
        db.session.commit()
    except  Exception as e:
      
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
       
    flash("Exercise deleted successfully" , "danger")
    return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))


@exercises_blueprint.route("/add_exercise_to_package" , methods=['POST'])
def add_exercises_to_package():
    Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
        ex_id = request.form.get('ex_id')
        pk_id = request.form.get('pk_id')
        
    if ex_id=='' or pk_id=='':
        flash("Exercise / Package cannot be empty" , "danger")
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))

    try:
        #db.session.execute("pragma foreign_keys=on")
        ex_pack = db.session.execute(f"INSERT INTO CONSISTS(PK_ID , EX_ID) VALUES( '{pk_id}' ,'{ex_id}' ) ")
        db.session.commit()
    except  Exception as e:
      
        db.session.rollback()
        flash("Exercises already added " , "danger" )
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
             
    flash("Exercise added to package successfully" , "success")
    return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))


@exercises_blueprint.route("/assign_exercise_to_trainer" , methods=['POST'])
def assign_exercise_to_trainer():
    Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
        ex_id = request.form.get('ex_id')
        tr_id = request.form.get('tr_id')
        
    if ex_id=='' or tr_id=='':
        flash("Exercise / Trainer cannot be empty" , "danger")
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))

    try:
        #db.session.execute("pragma foreign_keys=on")
        ex_trainer = db.session.execute(f"INSERT INTO CONDUCTS(TR_ID , EX_ID) VALUES( '{tr_id}' ,'{ex_id}' ) ")
        db.session.commit()
    except  Exception as e:
     
        db.session.rollback()
        flash("Exercises already assigned " , "danger" )
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
             
    flash("Exercise assigned to trainer successfully" , "success")
    return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))

@exercises_blueprint.route("/assign_exercise_to_member" , methods=['POST'])
def assign_exercise_to_member():
    Data_Paginate = EXERCISE.query.filter_by().paginate(per_page=5)

    if request.method == "POST":
        ex_id = request.form.get('ex_id')
        mem_id = request.form.get('mem_id')
        
    if ex_id=='' or mem_id=='':
        flash("Exercise / Member cannot be empty" , "danger")
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))

    try:
        #db.session.execute("pragma foreign_keys=on")
        ex_trainer = db.session.execute(f"INSERT INTO TAKEUP(MEM_ID , EX_ID) VALUES( '{mem_id}' ,'{ex_id}' ) ")
        db.session.commit()
    except  Exception as e:
      
        db.session.rollback()
        flash("Exercises already assigned " , "danger" )
        return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))
             
    flash("Exercise assigned to member successfully" , "success")
    return redirect(url_for('exercises.exercise',page_num=Data_Paginate.pages))