#!/usr/bin/env python3
"""Configuration module"""
from os import getenv
from dotenv import load_dotenv
from urllib.parse import quote

# Load environment variables from .env file
load_dotenv()

# MongoDB configuration
MONGODB_ADMIN = quote(getenv("MONGODB_ADMIN"), safe="")
MONGODB_ADMIN_PASSWORD = quote(getenv("MONGODB_ADMIN_PASSWORD"), safe="")
MONGODB_USER = quote(getenv("MONGODB_USER"), safe="")
MONGODB_PASSWORD = quote(getenv("MONGODB_PASSWORD"), safe="")
MONGODB_HOST = getenv("MONGODB_HOST")
MONGODB_PORT = getenv("MONGODB_PORT")
MONGODB_DATABASE = getenv("MONGODB_DATABASE")

# Get collections from environment variable and split them
DB_COLLECTIONS = getenv("DB_COLLECTIONS", "").split(",")
DB_COLLECTIONS = [collection.strip() for collection in DB_COLLECTIONS]

# URL encode the username and password
encoded_user = quote(MONGODB_USER, safe="")
encoded_password = quote(MONGODB_PASSWORD, safe="")

# Create database URI
MONGODB_URI = f"mongodb://{MONGODB_USER}:{MONGODB_PASSWORD}@{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}?authSource={MONGODB_DATABASE}"

# Flask configuration
SECRET_KEY = getenv("SECRET_KEY", "default_secret_key")

# Get Flask host IP and port number
WORKLOG_HOST = getenv("WORKLOG_HOST", "0.0.0.0")
WORKLOG_PORT = getenv("WORKLOG_PORT", "5000")
