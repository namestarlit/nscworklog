"""worklog User class"""

import re
import bcrypt
import string
import secrets

from worklog.base import Base


class User(Base):
    """Defines a User class for managing user data"""

    def __init__(self, username, email, password, *args, **kwargs):
        """Initializes an instance of User class"""
        super().__init__(*args, **kwargs)
        self.set_username(username)
        self.email = email
        self.password = password

    def __str__(self):
        """String representation of the User class"""
        return "[User] (id='{}', username='{}')".format(self._id, self.username)

    def set_username(self, username):
        """Setter for the username property"""
        if not self.is_valid_username(username):
            raise ValueError("Invalid username")
        self.username = username

    def is_valid_username(self, username):
        """Check if the provided username is of valid format"""
        # Only allow alphanumeric characters and underscores
        pattern = "^[a-z0-9_]+$"
        return bool(re.match(pattern, username))

    @property
    def email(self):
        """Getter for the email property"""
        return self.__email

    @email.setter
    def email(self, new_email):
        """Setter for the email property, with email format validation"""
        if not self.is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.__email = new_email

    def is_valid_email(self, email):
        """Check if the provided email has a valid format"""
        # A basic email format validation using regular expressions
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(email_pattern, email))

    @property
    def password(self):
        """Getter for the password property"""
        return self.__password

    @password.setter
    def password(self, new_password):
        """Setter for the password property"""
        # Hashes the provided password and stores it
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(new_password.encode("utf-8"), salt)
        self.__password = hashed_password

    def check_password(self, password):
        """Verify a provided password against the stored hash"""
        if self.__password:
            hashed_password = self.__password.encode("utf-8")
            password = password.encode("utf-8")
            return bcrypt.checkpw(password, hashed_password)
        return False

    def change_password(self, old_password, new_password):
        """Change the user's password to a new one"""
        # This will automatically call the setter
        if self.check_password(old_password):
            self.password = new_password
            return True
        return False

    def reset_password(self):
        """Reset the user password to a new password"""
        # set random password with 8 bytes
        new_password = self.generate_random_password(8)
        self.password = new_password
        return new_password

    @staticmethod
    def generate_random_password(length):
        """Generate a random password with the specified length"""
        characters = string.ascii_letters + string.digits + string.punctuation
        secure_password = "".join(secrets.choice(characters) for _ in range(length))
        return secure_password
