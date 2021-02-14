"""
This program runs a flask server with an interface.
To run the program:
   >> python run_app.py
Then:
   http://127.0.0.1:5000

It is tested on a development server.

Contact: Merve Unlu Menevse (m.merve.unlu@gmail.com)

"""

import sys
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/sockets/')
sys.path.insert(1,'/var/www/LectureQAapp/LectureQAapp/')

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,login_required, current_user
from flask import Blueprint
# main = Blueprint('main', __name__)

from .utils import get_questions, save_asked_questions, find_answer_in_video
from .statics import * 

from .sockets.appclient import run_client

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)


app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))
    
# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

#return app


@app.route('/')
def index():
    """
    The function generates the manin page.
    Gives a lecture video and the form.
    """
    return render_template('index.html')

if __name__== '__main__':
    create_app()
    app.run()
