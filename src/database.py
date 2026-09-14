import os
import sqlite3

# Default path to store the SQLite database
DB_PATH = os.path.join("data", "applications.db")

def init_db(db_path: str = DB_PATH):
    """Creates the SQLite database and sent_emails table if they do not exist."""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_email_sent(email: str, db_path: str = DB_PATH) -> bool:
    """Checks whether an email address has already received an application."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM sent_emails WHERE email = ?", (email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def log_sent_email(email: str, company: str, role: str, db_path: str = DB_PATH):
    """Logs a sent application into the database to prevent future duplicates."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO sent_emails (email, company, role)
        VALUES (?, ?, ?)
    ''', (email, company, role))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Quick module test
    init_db()
    print("Database initialized successfully!")

