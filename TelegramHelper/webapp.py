import os
from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Create db base class
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the Base
db = SQLAlchemy(model_class=Base)

# Create the Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key_for_testing")

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///loyalty.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the extension
db.init_app(app)

# Define User model to match the bot's database
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=True)
    first_name = db.Column(db.String, nullable=True)
    last_name = db.Column(db.String, nullable=True)
    hours = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, nullable=True)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users')
def users():
    users_list = User.query.all()
    return render_template('users.html', users=users_list)

@app.route('/api/users')
def api_users():
    users_list = User.query.all()
    result = []
    for user in users_list:
        result.append({
            'user_id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'hours': user.hours
        })
    return jsonify(result)

# Create database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)