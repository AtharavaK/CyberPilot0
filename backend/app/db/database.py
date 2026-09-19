import sqlite3
import os
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "cyberpilot.db")
DB_PATH = os.path.abspath(DB_PATH)

def init_db():
    """Create tables if they don't exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scans (
                scan_id     TEXT PRIMARY KEY,
                target_url  TEXT NOT NULL,
                status      TEXT NOT NULL DEFAULT 'INITIALIZING',
                overall_score INTEGER,
                created_at  DATETIME DEFAULT (datetime('now')),
                updated_at  DATETIME DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS findings (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id     TEXT NOT NULL,
                agent_name  TEXT NOT NULL,
                severity    TEXT NOT NULL,
                description TEXT NOT NULL,
                remediation TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            )
        """)
        conn.commit()
    print(f"[DB] Initialized SQLite database at: {DB_PATH}")

@contextmanager
def get_connection():
    """Thread-safe SQLite connection context manager."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
