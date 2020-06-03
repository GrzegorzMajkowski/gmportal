import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app=Flask(__name__)
app.config['SECRET_KEY']='mysecret'

##############################################
### DATABASE SETUP ###
##############################################
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
Migrate(app,db)
##############################################




##############################################
### LOGIN CONFIG ###
##############################################
login_manager = LoginManager() #login manager object creation
login_manager.init_app(app) # paasing app to login manager
login_manager.login_view='usersBP.login' #tell users what view to go to login , need to be creATED AND REGISTERED BLUPORINT FOR  USER -> LOGIN
##############################################




##############################################
### BLUEPRINT REGISTRATION ###
##############################################
from gmportal.core.views import coreBP
app.register_blueprint(coreBP)

from gmportal._users.views import usersBP
app.register_blueprint(usersBP)

from gmportal._losowa.views import losowaBP
app.register_blueprint(losowaBP)

from gmportal.views import startBP
app.register_blueprint(startBP)

# from puppycompanyblog.error_pages.handlers import error_pages
# app.register_blueprint(error_pages)

# from puppycompanyblog.users.views import users # blueprint zdefiniowany w user\views\ => users = Blueprint('users',__name__)
# app.register_blueprint(users)

# from puppycompanyblog.blog_posts.views import blog_posts
# app.register_blueprint(blog_posts)





