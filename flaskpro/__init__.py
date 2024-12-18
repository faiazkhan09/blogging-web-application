from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a090a3f473e55a134d124bc42b06b025'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # sets up database uri-> set to use sqlite and create & save a database called site.db, in the same folder as the main file(<- meaning of /// )
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'# type: ignore
login_manager.login_message_category = 'danger'

from flaskpro import routes