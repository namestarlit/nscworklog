"""Flask init methods"""
from flask import Flask
from flask_login import LoginManager
from configuration import Config


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"

# Initialize storage object
from worklog import dbstorage as storage


# Load user into flask session
@login.user_loader
def load_user(id):
    """Load the user into Flask's session"""
    user = storage.get("users", id)
    return user


from routes import routes, errors
