from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
from .models import Dog,User
from . import db 

views = Blueprint('views', __name__)
@views.route('/home')
@login_required
def home():
    return render_template("homepage.html",user = current_user)


@views.route('/rehome',methods=['GET','POST'])
@login_required
def rehome():
    if request.method=='POST':
        dogname=request.form.get('dogname')
        dogbreed=request.form.get('dogbreed')
        dogage=request.form.get('dogage')
        pincode=request.form.get('pincode')
        city=request.form.get('city')
        description=request.form.get('description')

        new_user = Dog(dogname=dogname,dogbreed=dogbreed,dogage=dogage,dogpincode=pincode,dogcity=city,dogdescription=description,dogownerid=current_user.id)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('views.home')) 

    return render_template("rehome.html",user=current_user)


@views.route('/adopt/',methods=['POST','GET'])
@login_required
def adoptq():
    users=User.query
    pincode = request.args.get("pincodesearch")
    breed = request.args.get("breedsearch")
    city = request.args.get("citysearch")
    if (pincode and not(breed) and not(city)):
        print("only pincode")
        dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%')).all()
        return render_template("adopt.html",dogs=dogs,users=users)
    elif(pincode and breed and not(city)):
        print("no city")
        dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%'),Dog.dogbreed.like('%'+breed+'%')).all()
        return render_template("adopt.html",dogs=dogs,users=users)
    elif(pincode and city and not(breed)):
        print("no breed")
        dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%'),Dog.dogcity.like('%'+city+'%')).all()
        return render_template("adopt.html",dogs=dogs,users=users)
    elif(pincode and breed and city):
        print("all")
        dogs=Dog.query.filter(Dog.dogpincode.like('%'+pincode+'%'),Dog.dogbreed.like('%'+breed+'%'),Dog.dogcity.like('%'+city+'%')).all()
        return render_template("adopt.html",dogs=dogs,users=users)
    else:
        return render_template("adopt.html")

