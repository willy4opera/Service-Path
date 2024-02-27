# Here we import all the packages that are required 
# By all the functions writtten in this module
from flask import Flask, flash, abort, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
import os
import secrets

# Here, we initialize or ORM
# The SQLAlchemy
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    upload_folder = os.path.join('static', 'uploads')
    app.config['UPLOAD'] = upload_folder
    app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.gif']
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Services
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


def save_profile(picture):
    app = create_app()
  
    filename = picture.filename
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            flash('file Extenstion not supported', category='error')
            return render_template("register.html", user=current_user)
            
            

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    
    if picture.save(picture_path):
        flash('Picture saved successfully', category='success')
    
    return picture_fn


