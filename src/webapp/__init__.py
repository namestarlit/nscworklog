from flask import Flask
from flask_login import LoginManager
from webapp.configuration import Config


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"

from webapp.models import forms
from webapp.routes import routes
from webapp.routes import errors
