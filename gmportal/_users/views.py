from flask import render_template, redirect, url_for, flash, request, Blueprint, escape
from flask_login import login_user, current_user, logout_user, login_required
from gmportal import db
from gmportal._users.models import User , LogLogin #, BlogPost
from gmportal._users.forms import RegistrationForm, LoginForm, UpdateUserForm
#from puppycompanyblog.users.picture_handler import add_profile_pic

usersBP = Blueprint('usersBP',__name__,template_folder='templates')

#login
@usersBP.route('/login', methods=['GET', 'POST'])
def login():
    
    form=LoginForm()
    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success!')
            u_remote_addr = request.remote_addr
            u_agent = escape(request.user_agent)
            loglog=LogLogin(user_id=current_user.id,user_email=current_user.email,user_username=current_user.username,user_role=current_user.role,user_remote_addr=u_remote_addr,user_agent=u_agent)
            db.session.add(loglog)
            db.session.commit()


            next=request.args.get('next')

            if next==None or not next[0]=='/':
                next=url_for('usersBP.index_auth')
            
            return redirect(next)
        else:
            return redirect(url_for('usersBP.bad_login'))

    return render_template('login.html', form=form)


@usersBP.route('/register' , methods=['GET', 'POST'])
def register():

    form=RegistrationForm()

    if form.validate_on_submit():
        user=User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('usersBP.login'))

    return render_template ('register.html', form=form)

@usersBP.route('/bad_login')
def bad_login():
    return render_template('login_bad.html')

@usersBP.route('/home')
@login_required
def index_auth():
    return render_template('index_auth.html', username=current_user.username)

@usersBP.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('coreBP.index'))






