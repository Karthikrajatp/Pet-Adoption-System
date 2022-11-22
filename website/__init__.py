from flask import Flask,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin,expose,BaseView,AdminIndexView
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

db=SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='usfeguaeghkejughkug1232455'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    db.init_app(app)
   
    from .views import views
    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(views, url_prefix='/')
    

    from .models import User,Dog
    with app.app_context():
        db.create_all()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    class myModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated

        def inaccessible_callback(self, name, **kwargs):
            return redirect(url_for('auth.login', next=request.url))
        
        def is_visible(self):
            return True     
    

    class HomeView(AdminIndexView):
        @expose("/")
        def index(self):
            return self.render('admin/homepage.html')

    
    admin.add_view(myModelView(User,db.session))
    admin.add_view(myModelView(Dog,db.session))


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app


