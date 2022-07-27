from pickle import NONE
from flask import Blueprint,render_template , flash, redirect, url_for, session, request, logging, make_response,jsonify
from flask import *
from app.models import *
from app.main import main
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from passlib.hash import sha256_crypt
from functools import wraps
from werkzeug.utils import secure_filename
from shutil import copyfile


auth_blueprint=Blueprint('auth',__name__)


##################################--Check-if-loggedin-####################################

#Decorator function to check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('auth.login'))
    return wrap

#####################################--Signin--###########################################

@auth_blueprint.route('/signin' , methods=['POST' , 'GET'])
def signin():
    if request.method=="POST":
        username=request.form.get("name")
        email=request.form.get("email")
        gid=request.form.get("gid")
        password=sha256_crypt.hash(str(request.form.get("pswd")))
 
        #query for gid for member/trainer
        #if gid doesnt exist flash error
        if gid[0] =='T':
            res=TRAINERS.query.filter(TRAINERS.T_GID==(gid)).first()
            if res is None:
                return render_template("/Dashboard/signin.html",msg="Invalid GYM ID Details",title="Login")

        elif gid[0] == 'M':
            res=MEMBERS.query.filter(MEMBERS.M_GID==(gid)).first()
            if res is None:
                return render_template("/Dashboard/signin.html",msg="Invalid GYM ID Details",title="Login")
        else:
                return render_template("/Dashboard/signin.html",msg="Invalid GYM ID Details",title="Login")
        
        
        #Set default profile pic whenever user signin
        
        my_data = UserData(username, email, password,gid)
        db.session.add(my_data)

        
        #Ensures whether username and email are unique
        try:
            db.session.commit()
        except IntegrityError:
            
            db.session.rollback()
            flash("Username/Email already exists! Try different name")
            return redirect(url_for('auth.signin'))

        flash("Signin Successfull!! Please Login")
        return redirect(url_for('auth.login'))

    return render_template("/Dashboard/signin.html",title="Signin")

#####################################--Login--############################################

@auth_blueprint.route('/login' , methods=['POST' , 'GET'])
def login():
    if request.method=="POST":
        username=request.form.get("name")
        email=request.form.get("email")
        gid=request.form.get("gid")
        remember = request.form.get("remember");
        password_candidate = request.form.get("pswd")
        
        #query for gid for member/trainer
        #if gid doesnt exist flash error
        
        
        
        if gid[0] =='T':
            res=TRAINERS.query.filter(TRAINERS.T_GID==(gid)).first()
            if res is None:
                return render_template("/Dashboard/login.html",msg="Invalid GYM ID Details",title="Login")

        elif gid[0] == 'M':
            res=MEMBERS.query.filter(MEMBERS.M_GID==(gid)).first()
            if res is None:
                return render_template("/Dashboard/login.html",msg="Invalid GYM ID Details",title="Login")
        else :
                return render_template("/Dashboard/login.html",msg="Invalid GYM ID Details",title="Login")
        
        
        #Get username and password from cookies
        usernam = request.cookies.get('usr')
        password_candidat = request.cookies.get('pwd')

        #Continue if details matches from cookies
        if 'usr' in request.cookies and (password_candidate == password_candidat) and (username == usernam):
            res=UserData.query.filter(UserData.U_NAME==(usernam)).first()

            if res is not None:
                 # Get stored hash
                password = res.U_PSWD

                # Compare Passwords
                #if sha256_crypt.verify(password_candidat, password):
                if password_candidat == password:
                    # Passed
                    session['logged_in'] = True
                    session['username'] = usernam
                    session['gid'] = gid
                    
                    flash('You are now logged in', 'success')
                    print("success")
                    return redirect(url_for('main.home'))
                else:
                    return render_template("/Dashboard/login.html",msg="Invalid password Details")
            else:

                return render_template("/Dashboard/login.html",msg="Invalid email/Password Details",title="Login")

        #If cookies doesnt exists
        elif username and password_candidate:

                    #Get user data of the entered username
                    res=UserData.query.filter(UserData.U_NAME==(username)).first()

                    if res is not None:
                        # Get stored hash
                        password = res.U_PSWD

                        # Compare Passwords
                        if sha256_crypt.verify(password_candidate, password):
                            #Set the session values
                            session['logged_in'] = True
                            session['username'] = username
                            session['gid'] = gid
                            #If user has clicked remember me set the cookies
                            if remember:
                                resp = make_response(redirect(url_for('main.home')))
                                resp.set_cookie('usr',username,max_age=current_app.config['COOKIE_TIME_OUT'])
                                resp.set_cookie('pwd',password,max_age=current_app.config['COOKIE_TIME_OUT'])
                                resp.set_cookie('rem','on',max_age=current_app.config['COOKIE_TIME_OUT'])
                                return resp

                            flash('You are now logged in', 'success')
                            flash("Hello")
                            print("success")
                            return redirect(url_for('main.home'))
                        else:
                            return render_template("/Dashboard/login.html",msg="Invalid password Details")
                    else:
                        return render_template("/Dashboard/login.html",msg="Invalid email/Password Details",title="Login")


    
    return render_template("/Dashboard/login.html",title="Login")

#######################################--Logout--#########################################

@auth_blueprint.route('/logout' , methods=['POST' , 'GET'])
@is_logged_in
def logout():
    #Clear the session once user logs out
    session.clear()

    flash('You are now logged out', 'success')
    return redirect(url_for('auth.login'))

########################################--Forgot-Password--##############################

@auth_blueprint.route('/reset' , methods=['POST'])
def forgot():
    email = request.form.get('email')
    new_password = request.form.get('new_password')
    print(email,new_password)

    #Query user data based on entered email
    res=UserData.query.filter(UserData.U_EMAIL==(email)).first()

    if res:
        res.U_PSWD=sha256_crypt.hash(str(new_password))
        db.session.commit()

        flash("Password reset successfully!! Please enter the new password")
        #Return json response to ajax call bcoz JS will recieve back redirect and render
        #template as result of call without changing DOM
        return jsonify({"status":"Password reset successfully"})
    else:
        return jsonify({"status":"Incorrect Email"})

