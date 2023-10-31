#import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
#from blog import routes
#from blueprint import blueprint


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f1f23a7bd6546b14141b273af62fd904'  # os.urandom(30)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:jayboy99@localhost:3306/mywinkappdb'
# app.register_blueprint(blueprint)
# app.register_blueprint(home)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'please login'
login_manager.login_message_category = 'info'

from blog import routes
