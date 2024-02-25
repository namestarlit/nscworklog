from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.validators import ValidationError

from worklog import storage


class LoginForm(FlaskForm):
    """A LoginForm class definition."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):
    """A RegistrationForm class definition."""

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """checks validation of username."""
        user = storage.get_user_by_filter("username", username)
        if user is not None:
            raise ValidationError(
                "username taken, please choose " "a different username"
            )

    def validate_email(self, email):
        """checks validation of email."""
        user = storage.get_user_by_filter("email", email)
        if user is not None:
            raise ValidationError(
                "email address already exists, " "please use a different email address."
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
                    "username taken, please choose " "a different username"
                )
