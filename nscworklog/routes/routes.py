from urllib.parse import urlparse
from flask import render_template, abort, jsonify
from flask import flash, redirect, request, url_for
from flask_login import login_user, logout_user
from flask_login import login_required, current_user

from nscworklog import app
from nscworklog import storage
from worklog.user import User
from worklog.worklog import Worklog
from forms import LoginForm, RegistrationForm
from forms import EditProfileForm, AddWorklogForm


@app.route("/")
def landing_page():
    """landing page"""
    return render_template("lp.html")


@app.route("/about")
def about_page():
    """About page"""
    return render_template("about.html", title="About")


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
            or urlparse(next_page).scheme != ""
            or urlparse(next_page).netloc != ""
        ):
            next_page = url_for("index")
        return redirect(next_page)

    login_page = render_template("login.html", title="Sign In", form=form)
    return login_page


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


@app.route("/logout")
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for("landing_page"))


@app.route("/home")
def index():
    """user homepage"""
    form = AddWorklogForm()

    return render_template("index.html", title="Home", form=form)


@app.route("/worklogs", methods=["POST"])
@login_required
def add_worklog():
    """Add worklog"""
    # Access form data from request.form
    title = request.form.get("title")

    if title:
        try:
            worklog = Worklog(title, current_user._id)
            worklog_id = storage.add(worklog)
            worklog = storage.get("worklogs", worklog_id)
            worklog = worklog.safe_dict()
            for key in ["created_at", "description", "user_id"]:
                worklog.pop(key, None)
        except Exception as e:
            abort(500, "Internal Server Error")

    return jsonify(worklog)


@app.route("/worklogs")
@login_required
def worklogs():
    """All User worklogs route"""
    try:
        worklogs = storage.all("worklogs", current_user._id)
        worklogs = [work.safe_dict() for work in worklogs]

        for worklog in worklogs:
            for key in ["created_at", "description", "user_id"]:
                worklog.pop(key, None)
    except Exception as e:
        abort(500, "Internal Server Error")

    return jsonify(worklogs)


@app.route("/worklogs/<worklog_id>", methods=["GET"])
@login_required
def get_worklog(worklog_id):
    """Gets a specific worklog"""
    worklog = storage.get("worklogs", worklog_id)
    worklog = worklog.safe_dict()
    worklog.pop("user_id", None)

    return jsonify(worklog)


@app.route("/worklogs/<worklog_id>/edit", methods=["GET"])
def edit_worklog(worklog_id):
    worklog = storage.get("worklogs", worklog_id)
    worklog = worklog.safe_dict()
    worklog.pop("user_id", None)

    # Render the HTML template with the worklog data
    return render_template("edit_worklog.html", worklog=worklog)


@app.route("/worklogs/<worklog_id>", methods=["POST"])
@login_required
def update_worklog(worklog_id):
    """Updates worklog info"""
    worklog = storage.get("worklogs", worklog_id)

    if not worklog:
        abort(404, "Worklog not found")

    form_data = request.form

    worklog.title = form_data.get("title")
    worklog.description = form_data.get("description")
    worklog.status = form_data.get("status")

    # Process extras, assuming extras is a dictionary
    new_extras = {}

    for key, value in form_data.items():
        if key not in ["title", "description", "status"]:
            if key.startswith("key-"):
                # Split the key to get the index part
                key_parts = key.split("-")
                if len(key_parts) == 2 and key_parts[0] == "key":
                    index = key_parts[1]
                    value_key = f"value-{index}"
                    # Check if the corresponding value exists
                    if value_key in form_data:
                        new_value = form_data[value_key]
                        # Only add to new_extras if the value is not empty
                        if new_value.strip():
                            new_extras[value] = new_value
                        elif hasattr(worklog, "extras") and new_value in worklog.extras:
                            del worklog.extras[new_value]
            else:
                if (
                    not value.strip()
                    and hasattr(worklog, "extras")
                    and key in worklog.extras
                ):
                    del worklog.extras[key]

    # Check if the worklog object has the
    if hasattr(worklog, "extras"):
        worklog.extras.update(**new_extras)
    else:
        worklog.extras = new_extras

    storage.update(worklog._id, worklog)

    updated_worklog = {
        "title": worklog.title,
        "description": worklog.description,
        "extras": worklog.extras,
    }

    return jsonify(updated_worklog)


@app.route("/worklogs/<worklog_id>", methods=["DELETE"])
@login_required
def delete_worklog(worklog_id):
    """Delete a worklog"""
    worklog = storage.get("worklogs", worklog_id)

    try:
        storage.delete("worklogs", worklog._id)
    except Exception as e:
        abort(500, "Internal Server Error")

    return jsonify({})
