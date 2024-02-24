from webapp import app

@app.route("/")
def index():
    """homepage"""
    return "Welcome to Worklog"
