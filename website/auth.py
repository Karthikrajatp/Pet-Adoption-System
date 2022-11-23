from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

auth = Blueprint('auth', __name__)
@auth.route('/',methods=['GET','POST'])
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user,remember=True)
                if user.id == 1:
                    return redirect('/admina')
                return redirect(url_for('views.home'))  
            else:
                flash("Incorrect Password,Try again!!",category='error')
        else:
            flash("User does not exist!!",category='error')
    return render_template("loginpage.html",boolean = True)

@auth.route('/admina')
@login_required
def admin():
    return redirect("/admin")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("LoggedOut successfully!!")
    return redirect(url_for('auth.login'))
    
@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        fullname=request.form.get('fullname')
        username=request.form.get('username')
        email=request.form.get('email')
        phonenumber=request.form.get('phonenumber')
        password1=request.form.get('password')
        password2=request.form.get('confirmpassword')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists",category='error')
        elif len(email)<5:
            flash("Your e-mail is too short!!",category='error')
        elif (len(username) or len(fullname))<5:
            flash("Your Name is too short!!,try to increase the characters",category='error')
        elif len(phonenumber)<=10:
            flash("Please Enter a valid mobile number",category='error')
        elif len(password1)<7:
            flash("Your Password is too weak!!",category='error')
        elif password1!=password2:
            flash("Your Passwords don't match!!",category='error')
        else:
            new_user = User(fullname=fullname,username=username,email=email,phonenumber=phonenumber,password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash("Account created!!",category='success')
            return redirect(url_for('auth.login'))
    
    return render_template("registrationpage.html")

