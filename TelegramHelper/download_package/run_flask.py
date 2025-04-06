"""
Simple script to run the Flask app directly for testing
"""
from app import app

if __name__ == "__main__":
    print("Starting Flask application on http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)