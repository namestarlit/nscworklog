from flask import Flask
from flask_login import LoginManager
from webapp.configuration import Config


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

login = LoginManager(app)

from webapp.routes import routes
