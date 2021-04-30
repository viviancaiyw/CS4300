# Gevent needed for sockets
from gevent import monkey
monkey.patch_all()

# Imports
import os
import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_login import LoginManager


# Configure app
socketio = SocketIO()
app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# DB
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# login
login = LoginManager(app)
login.login_view = 'register'

# Import + Register Blueprints
from app.accounts import accounts as accounts
app.register_blueprint(accounts)
from app.irsystem import irsystem as irsystem
app.register_blueprint(irsystem)

# Initialize app w/SocketIO
socketio.init_app(app)

# modules import
# route / User
# from app.utilities import routes
from app.accounts.models.user import User

# HTTP error handling
@app.errorhandler(404)
def not_found(error):
  return render_template("404.html", error=error), 404

@app.shell_context_processor
def make_shell_context():
  return {'db':db, 'User':User}
