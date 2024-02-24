from webapp import app
from worklog import storage

@app.route("/")
def index():
    """homepage"""
    return "Welcome to Worklog"
