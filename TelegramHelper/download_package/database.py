import sqlite3
import logging
from config import DB_PATH

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        """Initialize database connection and cursor"""
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Connect to the SQLite database"""
        try:
            self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            logger.info("Database connection established")
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise

    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    hours REAL DEFAULT 0,
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Add language column if it doesn't exist
            try:
                self.cursor.execute("SELECT language FROM users LIMIT 1")
            except sqlite3.OperationalError:
                logger.info("Adding language column to users table")
                self.cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
            
            # Create a table for tracking hour logs
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS hour_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    hours REAL,
                    confirmed BOOLEAN DEFAULT 0,
                    confirmed_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            self.conn.commit()
            logger.info("Database tables initialized")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            raise

    def get_user(self, user_id):
        """Get user by ID"""
        try:
            self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    def create_user(self, user_id, username=None, first_name=None, last_name=None, language='en'):
        """Create a new user record"""
        try:
            self.cursor.execute(
                "INSERT INTO users (user_id, username, first_name, last_name, hours, language) VALUES (?, ?, ?, ?, 0, ?)",
                (user_id, username, first_name, last_name, language)
            )
            self.conn.commit()
            logger.info(f"Created new user: {user_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error creating user {user_id}: {e}")
            return False

    def update_hours(self, user_id, hours):
        """Update user hours"""
        try:
            self.cursor.execute("UPDATE users SET hours = ? WHERE user_id = ?", (hours, user_id))
            self.conn.commit()
            logger.info(f"Updated hours for user {user_id} to {hours}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating hours for user {user_id}: {e}")
            return False

    def get_user_hours(self, user_id):
        """Get hours for a user"""
        try:
            self.cursor.execute("SELECT hours FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result["hours"] if result else 0
        except sqlite3.Error as e:
            logger.error(f"Error getting hours for user {user_id}: {e}")
            return 0

    def update_user_language(self, user_id, language_code):
        """Update user's preferred language"""
        try:
            self.cursor.execute("UPDATE users SET language = ? WHERE user_id = ?", (language_code, user_id))
            self.conn.commit()
            logger.info(f"Updated language for user {user_id} to {language_code}")
            return True
        except sqlite3.Error as e:
            logger.error(f"Error updating language for user {user_id}: {e}")
            return False
    
    def get_user_language(self, user_id):
        """Get language preference for a user"""
        try:
            self.cursor.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
            result = self.cursor.fetchone()
            return result["language"] if result else 'en'
        except sqlite3.Error as e:
            logger.error(f"Error getting language for user {user_id}: {e}")
            return 'en'
    
    def log_hours(self, user_id, hours):
        """Log hours for a user (before confirmation)"""
        try:
            self.cursor.execute(
                "INSERT INTO hour_logs (user_id, hours) VALUES (?, ?)",
                (user_id, hours)
            )
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            logger.error(f"Error logging hours for user {user_id}: {e}")
            return None
    
    def confirm_hours(self, log_id, admin_id):
        """Confirm hours by admin"""
        try:
            self.cursor.execute(
                "UPDATE hour_logs SET confirmed = 1, confirmed_by = ? WHERE id = ?",
                (admin_id, log_id)
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Error confirming hours log {log_id}: {e}")
            return False
    
    def get_user_hour_logs(self, user_id, limit=10):
        """Get recent hour logs for a user"""
        try:
            self.cursor.execute(
                "SELECT * FROM hour_logs WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit)
            )
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting hour logs for user {user_id}: {e}")
            return []
    
    def get_all_users(self):
        """Get all users"""
        try:
            self.cursor.execute("SELECT * FROM users ORDER BY hours DESC")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logger.error(f"Error getting all users: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
