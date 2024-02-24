from flask import Flask
from webapp.configuration import Config


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

from webapp.routes import routes
