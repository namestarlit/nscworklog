#!/usr/bin/env python3
"""MongoDB setup"""
from pymongo import MongoClient
from config import MONGODB_URI
from config import (
    MONGODB_USER,
    MONGODB_PASSWORD,
    MONGODB_ADMIN,
    MONGODB_ADMIN_PASSWORD,
    MONGODB_DATABASE,
)


# Connect to the MongoDB server
client = MongoClient(MONGODB_URI)

# Switch to the admin database (required for creating users)
admin_db = client.admin

# Create a regular user
admin_db.command(
    "createUser",
    MONGODB_USER,
    pwd=MONGODB_PASSWORD,
    roles=[{"role": "readWrite", "db": MONGODB_DATABASE}],
)

# Create an admin user
admin_db.command(
    "createUser",
    MONGODB_ADMIN,
    pwd=MONGODB_ADMIN_PASSWORD,
    roles=[
        {"role": "userAdminAnyDatabase", "db": "admin"},
        {"role": "readWriteAnyDatabase", "db": "admin"},
    ],
)

# Close the connection
client.close()
