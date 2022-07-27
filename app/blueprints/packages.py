from flask import Blueprint,render_template
from flask import *
from app.models import *

packages_blueprint=Blueprint('packages',__name__)


@packages_blueprint.route('/' ,  methods=['POST' , 'GET'])
@packages_blueprint.route('/<int:page_num>' ,  methods=['POST' , 'GET'])
def package(page_num=1):
    count = db.engine.execute(f"SELECT count('P_ID') from PACKAGE").scalar()

    exercises_in_package = db.session.execute("SELECT EXERCISE.E_NAME , PACKAGE.P_NAME , CONSISTS.PK_ID , CONSISTS.EX_ID FROM CONSISTS JOIN EXERCISE ON CONSISTS.EX_ID = EXERCISE.E_ID JOIN PACKAGE ON CONSISTS.PK_ID = PACKAGE.P_ID")
    exercises_in_package_tuples = [row for row in exercises_in_package]
    
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form.get('tag')
        search = "%{}%".format(tag)
        employees = PACKAGE.query.filter(PACKAGE.P_NAME.like(search)).paginate(per_page=5, error_out=False)
        context={
            'icon' : "glyphicon-list-alt" ,
            'ex_tuples' : exercises_in_package_tuples,
            'ispackages' : "active" , 
            'title' : "Packages" , 
            'rows' : PACKAGE.query.all() , 
            'Data_Paginate' : employees , 
            'isact' : "active" , 
            'pcount' : count 
        }
        return render_template('/Dashboard/packages.html' , **context)



    Data_Paginate = PACKAGE.query.filter_by().paginate(per_page=5,page=page_num , error_out = False)
    context = {
         'icon' : "glyphicon-list-alt" ,
         'ex_tuples' :  exercises_in_package_tuples ,
         'ispackages' : "active" ,
         'title' : "Packages" ,
         'rows' : PACKAGE.query.all() ,
         'Data_Paginate' : Data_Paginate ,
         'isact' : "active" ,
         'pcount' : count 
    }
    return render_template('/Dashboard/packages.html' , **context)


@packages_blueprint.route('/add_package' , methods=['POST'])
def add_package():
   Data_Paginate = PACKAGE.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       p_name = request.form.get("p_name")
       p_price = request.form.get("p_price")
       p_duration = request.form.get("p_duration")

       try:
           package = db.engine.execute(f"INSERT INTO PACKAGE(P_NAME , P_PRICE ,P_DURATION) VALUES( '{p_name}' ,'{p_price}' ,'{p_duration}' ) ")
       except  Exception as e:
           db.session.rollback()
           flash("Package already exists" , "danger" )
           return redirect(url_for('packages.package',page_num=Data_Paginate.pages))
             
   flash("Package added successfully" , "success")
   return redirect(url_for('packages.package',page_num=Data_Paginate.pages))


@packages_blueprint.route('/edit_package/<int:p_id>' , methods=['POST'])
def edit_package(p_id):
   Data_Paginate = PACKAGE.query.filter_by().paginate(per_page=5)

   if request.method == "POST":
       p_name = request.form.get("p_name")
       p_price = request.form.get("p_price")
       p_duration = request.form.get("p_duration")

       try:
           package = db.engine.execute(f"Update  PACKAGE SET P_NAME='{p_name}' , P_PRICE= '{p_price}'  , P_DURATION='{p_duration}'  where P_ID ='{p_id}'")
       except  Exception as e:
           db.session.rollback()
           flash("Some error occured" , "danger" )
           return redirect(url_for('packages.package',page_num=Data_Paginate.pages))
             
   flash("Package updated successfully" , "success")
   return redirect(url_for('packages.package',page_num=Data_Paginate.pages))

@packages_blueprint.route('/delete_package/<int:p_id>' )
def delete_package(p_id):
    Data_Paginate = PACKAGE.query.filter_by().paginate(per_page=5)
    
    try:
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM PACKAGE WHERE PACKAGE.P_ID = {p_id}")
        db.session.commit()
    except  Exception as e:
     
        db.session.rollback()
        flash("Some error occured" , "danger" )
        return redirect(url_for('packages.package',page_num=Data_Paginate.pages))
       
    flash("Package deleted successfully" , "danger")
    return redirect(url_for('packages.package',page_num=Data_Paginate.pages))

@packages_blueprint.route('/delete_consist/<ck>' )
def delete_consist(ck):
    keys = ck.split(' ');
    
    Data_Paginate = PACKAGE.query.filter_by().paginate(per_page=5)
    
    try:
        #fk_check = db.session.execute("pragma foreign_keys=on");
        db.session.execute(f"DELETE FROM CONSISTS WHERE CONSISTS.PK_ID = {keys[0]} AND CONSISTS.EX_ID = {keys[1]} ")
        db.session.commit()
    except  Exception as e:
     
        db.session.rollback()
        flash("Some error occured" , "danger")
        return redirect(url_for('packages.package',page_num=Data_Paginate.pages))
    return "[]"