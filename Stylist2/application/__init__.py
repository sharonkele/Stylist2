from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY']='f9bf78ba18ce6d46a0cd2b0b86df9da'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from application import routes 