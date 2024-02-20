#!/usr/bin/env python3
"""Generate Flask sercret key"""
import string
import secrets


def generate_flask_secret_key():
    # Flask secret key should be a 24-byte (192-bit) string
    secret_key = secrets.token_hex(24)
    return secret_key


def generate_database_user_password():
    """Generate a random password with the specified length"""
    password_length = 12
    characters = string.ascii_letters + string.digits + string.punctuation
    secure_password = "".join(
        secrets.choice(characters) for _ in range(password_length)
    )

    return secure_password


if __name__ == "__main__":
    # Generate a random Flask secret key
    flask_secret_key = generate_flask_secret_key()

    # Print or use the generated key as needed
    print(f"Generated Flask Secret Key: {flask_secret_key}")

    # Generate a random database user password
    database_password_0 = generate_database_user_password()
    database_password_1 = generate_database_user_password()

    # Print or use the generated password as needed
    print(f"Generated Database User Password: {database_password_0}")
    print(f"Generated Database User Password: {database_password_1}")
