#core/views.py


from flask import render_template, redirect, url_for, flash, request, Blueprint, escape
from flask_login import login_user, current_user, logout_user, login_required
from gmportal import db
from gmportal._users.models import User , LogLogin #, BlogPost
from gmportal._users.forms import RegistrationForm, LoginForm, UpdateUserForm
from gmportal._losowa.models import LosowaTab




#from puppycompanyblog.models import BlogPost

coreBP=Blueprint('coreBP',__name__,template_folder='templates')


@coreBP.route('/settings')
def settings():
    # more to come
    return render_template('settings.html')

@coreBP.route('/info')
def info():
    return render_template('info.html')


@coreBP.route('/logina')
def login():
    return render_template('logina.html')

@coreBP.route('/create-new-db-once-only')
def create_db():
    db.create_all()
    return redirect(url_for('startBP.index'))