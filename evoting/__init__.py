from flask import Flask
import flask_login
from evoting.voting import *

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

login_manager = flask_login.LoginManager(app)

my_voting = Voting(['Kandydat1', 'Kandydat2', 'Kandydat3', 'Kandydat4'], False)
my_voting.generate_keys(2048)
voters = []

# Startapp
from evoting import routes
