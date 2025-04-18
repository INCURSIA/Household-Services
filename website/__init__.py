from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .adm import adm
    from .proff import proff
    from .custo import custo

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(adm, url_prefix = '/')
    app.register_blueprint(proff, url_prefix = '/')
    app.register_blueprint(custo, url_prefix = '/')


    from . import models
    from .models import User
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'views.home'
    login_manager.init_app(app)

    from .models import User,Professional
    @login_manager.user_loader
    def load_user(user_email):
        user = User.query.get(user_email)
        if user:
            return user

        professional = Professional.query.get(user_email)
        if professional:
            return professional

        return None  


    


    return app
def create_database(app):
    with app.app_context(): 
        if not path.exists('website/' + DB_NAME):
            db.create_all() 
            print('Created Database!')

