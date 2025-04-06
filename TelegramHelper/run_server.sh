#!/bin/bash
# This script runs the Flask web application using Gunicorn

echo "==================================="
echo "= Starting Studio Hours Web Server ="
echo "==================================="

# Kill any existing Gunicorn processes
pkill -f gunicorn || true

# Start the web application with Gunicorn
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload app:app

echo "Web application stopped"