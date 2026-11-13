
import sqlite3
from pathlib import Path


# Database file location
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "finance.db"


def get_connection():
    """Create and return a SQLite database connection."""

    connection = sqlite3.connect(DATABASE_PATH)

    # Return database rows as dictionary-like objects
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def create_tables():
    """Create application database tables."""

    connection = get_connection()

    cursor = connection.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            amount_paise INTEGER NOT NULL
                CHECK (amount_paise > 0),

            type TEXT NOT NULL
                CHECK (type IN ('Income', 'Expense')),

            category TEXT NOT NULL,

            date TEXT NOT NULL,

            notes TEXT DEFAULT '',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT NOT NULL,

            amount_paise INTEGER NOT NULL
                CHECK (amount_paise > 0),

            month TEXT NOT NULL,

            UNIQUE(category, month)
        )
    """)

    connection.commit()

    connection.close()

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()
if __name__ == "__main__":
    create_tables()

    connection = get_connection()

    tables = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    print("Available tables:")

    for table in tables:
        print(table["name"])

    connection.close()