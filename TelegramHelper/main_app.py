"""
Main web application entry point for Gunicorn.
This file is needed for the Replit workflow to find the app object.
"""
from app import app

# This variable is what Gunicorn looks for when starting the application
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)