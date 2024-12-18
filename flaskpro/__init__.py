from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a090a3f473e55a134d124bc42b06b025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'# type: ignore
login_manager.login_message_category = 'danger'

from flaskpro import routes
