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


    # MEMORY
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


    # FILES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT NOT NULL,

            file_name TEXT NOT NULL,

            drive_file_id TEXT NOT NULL,

            mime_type TEXT,

            drive_link TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)


    conn.commit()

    conn.close()