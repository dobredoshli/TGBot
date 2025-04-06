"""
Main web application entry point.
This file is needed to run the web application via the workflow.
"""

from app import app

# This import is needed for the workflow to successfully find the app object
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)