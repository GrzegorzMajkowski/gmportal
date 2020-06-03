from gmportal import db, login_manager #import login manager from __init_.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin #functionality is autenthicated, is acive etc...
from datetime import datetime

## after importing login manager
## function that allows us to say that user is authenticated
## login manager and user loader activated in __init__.py
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model, UserMixin):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(20),nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash=db.Column(db.String(128))
    role = db.Column(db.String(30),nullable=False, default='user')
    

    #post = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email=email
        self.username=username
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f'Username: {self.username}, Role: {self.role}'


class LogLogin(db.Model, UserMixin):
    __tablename__='loglogin'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_email = db.Column(db.String(64))
    user_username = db.Column(db.String(64))
    user_role = db.Column(db.String(30))
    login_date = db.Column(db.DateTime,nullable=False, default=datetime.now)
    user_remote_addr = db.Column(db.String(128))
    user_agent = db.Column(db.String(128))

    def __init__(self, user_id, user_email, user_username, user_role, user_remote_addr = '-', user_agent='-'):
        self.user_id=user_id
        self.user_email=user_email
        self.user_username=user_username
        self.user_role=user_role
        self.user_remote_addr=user_remote_addr
        self.user_agent=user_agent
        


