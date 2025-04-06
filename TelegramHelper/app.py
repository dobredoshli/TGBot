import os
import sqlite3
from flask import Flask, jsonify, Response, render_template_string

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_testing")

# Define database connection
DB_PATH = os.path.join(os.path.dirname(__file__), 'loyalty.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# HTML template (inline)
INDEX_HTML = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Studio Hours Tracker</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Studio Hours Tracker</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/users">Users</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <div class="card">
                    <div class="card-header">
                        <h2>Studio Hours Tracker Admin Panel</h2>
                    </div>
                    <div class="card-body">
                        <h5 class="card-title">Welcome to the Studio Hours Tracker!</h5>
                        <p class="card-text">This web interface allows administrators to view and manage user studio hours tracked by the Telegram bot.</p>
                        <div class="d-grid gap-2">
                            <a href="/users" class="btn btn-primary">View Users</a>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <h4>Bot Features</h4>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">Track studio hours for users</li>
                            <li class="list-group-item">Admin approval for logged hours</li>
                            <li class="list-group-item">Automatic reward system for accumulated hours</li>
                            <li class="list-group-item">User-friendly interface with Telegram bot</li>
                        </ul>
                    </div>
                </div>
                
                <div class="card mt-4">
                    <div class="card-header">
                        <h4>How It Works</h4>
                    </div>
                    <div class="card-body">
                        <ol class="list-group list-group-numbered">
                            <li class="list-group-item">Users log their studio hours through the Telegram bot</li>
                            <li class="list-group-item">Admins receive notifications and approve or reject the request</li>
                            <li class="list-group-item">Approved hours are added to the user's account</li>
                            <li class="list-group-item">Every 8 hours, users earn a free session</li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <p class="text-center mb-0">© 2025 Studio Hours Tracker. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

USERS_HTML = """
<!DOCTYPE html>
<html lang="en" data-bs-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Users - Studio Hours Tracker</title>
    <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Studio Hours Tracker</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="/">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link active" aria-current="page" href="/users">Users</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-5">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h2>User List</h2>
                        <a href="/" class="btn btn-secondary">Back to Home</a>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead>
                                    <tr>
                                        <th>User ID</th>
                                        <th>Username</th>
                                        <th>Name</th>
                                        <th>Hours</th>
                                        <th>Free Sessions</th>
                                        <th>Hours Until Next Free</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for user in users %}
                                    <tr>
                                        <td>{{ user.user_id }}</td>
                                        <td>{{ user.username or '-' }}</td>
                                        <td>
                                            {% if user.first_name or user.last_name %}
                                                {{ user.first_name or '' }} {{ user.last_name or '' }}
                                            {% else %}
                                                -
                                            {% endif %}
                                        </td>
                                        <td>{{ user.hours|round(2) }}</td>
                                        <td>{{ (user.hours // 8)|int }}</td>
                                        <td>{{ 8 - (user.hours % 8)|round(2) }}</td>
                                    </tr>
                                    {% endfor %}
                                    {% if not users %}
                                    <tr>
                                        <td colspan="6" class="text-center">No users found</td>
                                    </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer class="bg-dark text-light py-4 mt-5">
        <div class="container">
            <p class="text-center mb-0">© 2025 Studio Hours Tracker. All rights reserved.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

# Routes
@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/users')
def users():
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        
        # Convert to list of dicts
        user_list = [dict(user) for user in users]
        
        return render_template_string(USERS_HTML, users=user_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users')
def api_users():
    try:
        conn = get_db_connection()
        users = conn.execute('SELECT * FROM users').fetchall()
        conn.close()
        
        # Convert to list of dicts
        result = []
        for user in users:
            result.append({
                'user_id': user['user_id'],
                'username': user['username'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'hours': user['hours']
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Starting web application on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)