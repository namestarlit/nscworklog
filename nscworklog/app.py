#!/usr/bin/env python3
"""main application"""
from nscworklog import app
from config import WORKLOG_HOST, WORKLOG_PORT


if __name__ == "__main__":
    # Run the application
    app.run(host=WORKLOG_HOST, port=WORKLOG_PORT, threaded=True)
