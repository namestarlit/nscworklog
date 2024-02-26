from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import ValidationError

from nscworklog import storage


class LoginForm(FlaskForm):
    """A LoginForm class definition."""

    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your password"},
    )
    remember_me = BooleanField("Remember_me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """A RegistrationForm class definition."""

    username = StringField(
        "Username",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter your username"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Enter your email"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    password_2 = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"placeholder": "Confirm password"},
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """checks validation of username."""
        user = storage.get_user_by_filter("username", username)
        if user is not None:
            raise ValidationError(
                "Username taken, " "please choose a different username."
            )

    def validate_email(self, email):
        """checks validation of email."""
        user = storage.get_user_by_filter("email", email)
        if user is not None:
            raise ValidationError(
                "Email address already exists, " "please use a different email address."
            )


class EditProfileForm(FlaskForm):
    """A EditProfileForm class definition."""

    username = StringField("Username", validators=[DataRequired()])
    submit = SubmitField("Save")

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = storage.get_user_by_filter("username", username)
            if user is not None:
                raise ValidationError(
                    "Username taken, " "please choose a different username."
                )
