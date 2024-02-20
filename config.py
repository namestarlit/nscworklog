#!/usr/bin/env python3
"""Configuration module"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# MongoDB configuration
MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")

# Other shared configuration variables
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
