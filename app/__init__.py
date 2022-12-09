from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_admin import Admin
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

admin = Admin(app, template_mode='bootstrap4')

migrate = Migrate(app, db)

# Initialise bootstrap and csrf
Bootstrap(app)
csrf = CSRFProtect(app)

#Initialises the login manager for the chatty forums
login_manager = LoginManager()
login_manager.login_view = 'loginPage'
login_manager.init_app(app)

from .models import User

#Defining load_user so that the login manager can find the user trying to log in
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import views, models