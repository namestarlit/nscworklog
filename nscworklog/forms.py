from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import BooleanField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import ValidationError

from nscworklog import storage


class LoginForm(FlaskForm):
    """A LoginForm class definition."""

    username = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    password = PasswordField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    remember_me = BooleanField("Remember_me")
    submit = SubmitField("Sign In")

    def validate_username(self, username):
        """checks validation of username & password."""

        user = storage.get_user_by_filter("username", username.data)
        if user is None :
            raise ValidationError(
                "Invalid username or password."
            )


class RegistrationForm(FlaskForm):
    """A RegistrationForm class definition."""

    username = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    email = StringField(
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )
    password = PasswordField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    password_2 = PasswordField(
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """checks validation of username."""

        user = storage.get_user_by_filter("username", username.data)
        if user is not None:
            raise ValidationError(
                "Username taken, " "please choose a different username."
            )

    def validate_email(self, email):
        """checks validation of email."""
        user = storage.get_user_by_filter("email", email.data)
        if user is not None:
            raise ValidationError(
                "Email address already exists, " "please use a different email address."
            )


class EditProfileForm(FlaskForm):
    """A EditProfileForm class definition."""

    username = StringField(validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = storage.get_user_by_filter("username", username.data)
            if user is not None:
                raise ValidationError(
                    "Username taken, " "please choose a different username."
                )

class AddWorklogForm(FlaskForm):
    """Adds a new worklog entry"""

    title = StringField(
        validators=[DataRequired()],
        render_kw={"placeholder": "Add a worklog, press [ Enter ] to save"},
    )

class ExtrasForm(FlaskForm):
    key = StringField('Key')
    value = StringField('Value')

class WorklogForm(FlaskForm):
    """Displays worklog details"""

    title = StringField('Title')
    description = TextAreaField('Description')
    extras = FieldList(FormField(ExtrasForm), min_entries=1)

    save = SubmitField('Save')
