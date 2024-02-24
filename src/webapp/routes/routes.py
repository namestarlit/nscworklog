from urllib.parse import urlparse
from flask_login import current_user
from flask import render_template, abort, jsonify
from flask import flash, redirect, request, url_for
from flask_login import login_required, login_user, logout_user

from webapp import app
from worklog import storage
from webapp.models.user import User
from webapp.models.forms import LoginForm, RegistrationForm, EditProfileForm


@app.route("/")
def landing_page():
    """landing page"""
    return "Welcome to nscworklog" ""


@app.route("/home")
def index():
    """user homepage"""
    worklogs = storage.all("worklogs", user_id)
    worklogs = [work.to_dict() for work in worklogs]

    for worklog in worklogs:
        for key in ["_id", "created_at", "updated_at", "user_id"]:
            worklog.pop(key, None)

    return jsonify(worklogs)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = storage.get_user_by_filter("username", form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if (
            not next_page
            or urlparse(next_url).scheme != ""
            or urlparse(next_url).netloc != ""
        ):
            next_page = url_for("index")
        return redirect(next_page)

    login_page = render_template("login.html", title="Sign In", form=form)
    return login_page


@app.route("/logout")
def logout():
    """Logout route"""
    logout_user()

    return redirect(url_for("landing_page"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register route"""
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        try:
            # Add user to the database
            storage.add(user)
            flash("Congratulations, you are now a registered user!")

            # Redirect user to login page
            return redirect(url_for("login"))
        except Exception as e:
            abort(500, "Internal Server Error")

    register_page = render_template("register.html", title="Sign Up", form=form)

    return register_page


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """User profile route"""
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        try:
            current_user.username = form.username.data
            storage.update(current_user)
            flash("Your changes have been saved")

            return redirect(url_for("profile"))
        except Exception as e:
            abort(500, "Internal Server Error")
    elif request.method == "GET":
        form.username.data = current_user.username

    profile_page = render_template("profile.html", title="Profile", form=form)

    return profile_page


@app.route("/worklogs")
def worklogs():
    """All User worklogs route"""
    try:
        worklogs = storage.all("worklogs", current_user._id)
        worklogs = [work.safe_dict() for work in worklogs]

        for worklog in worklogs:
            for key in ["_id", "created_at", "updated_at", "user_id"]:
                worklog.pop(key, None)
    except Exception as e:
        abort(500, "Internal Server Error")

    return jsonify(worklogs)


@app.route("/worklogs/<worklog_id>")
def worklog(worklog_id):
    """Gets a user's worklog"""
    worklog = storage.get("worklogs", worklog_id)

    return jsonify(worklog.safe_dict())
