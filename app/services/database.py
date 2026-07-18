import sqlite3
from pathlib import Path


DB_PATH = Path("data/dot_ai.db")

DB_PATH.parent.mkdir(exist_ok=True)


def get_connection():

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def init_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            UNIQUE(user_id, key)
        )
    """)

    conn.commit()

    conn.close()