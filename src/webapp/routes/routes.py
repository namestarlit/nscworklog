from webapp import app
from flask import render_template, jsonify
from worklog import storage


@app.route("/")
def homepage():
    """homepage"""
    return "Welcome to nscworklog"""


@app.route("/<user_id>")
def index(user_id):
    """user homepage"""
    worklogs = storage.all("worklogs", user_id)
    worklogs = [work.to_dict() for work in worklogs]

    for worklog in worklogs:
        for key in ["_id", "created_at", "updated_at", "user_id"]:
            worklog.pop(key, None)

    return jsonify(worklogs)
