from webapp import login
from flask_login import UserMixin

from worklog import storage
from worklog.user import User


@login.user_loader
def load_user(id):
    """Load the user into Flask's session"""
    user = storage.get("users", id)
    return user


class User(UserMixin, User):
    """User class implementantion"""

    def __init__(self, username, email, password, *args, **kwargs):
        """Initializes an instance of User class"""
        super().__init__(username, email, password, *args, **kwargs)

    def avatar(self, size):
        """Gets a user's profile picture."""
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"
