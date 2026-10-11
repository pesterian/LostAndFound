import sqlite3
from pathlib import Path

# Database path (stored in backend directory)
DB_PATH = Path(__file__).resolve().parent.parent / "lost_and_found.db"


def get_db_connection() -> sqlite3.Connection:
    """
    Creates and returns a raw sqlite3 connection.
    row_factory is set to sqlite3.Row for convenient dict-like column access.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Ensure foreign keys are enforced in SQLite
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    """
    Initialize database tables with explicit raw SQL strings.
    TODO: Add table creation statements here once the team finalizes the ERD.
    Example:
        conn = get_db_connection()
        try:
            with conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        ...
                    );
                ''')
        finally:
            conn.close()
    """
    pass

