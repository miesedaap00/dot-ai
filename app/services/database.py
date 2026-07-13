import sqlite3
from pathlib import Path

Path("data").mkdir(exist_ok=True)

conn = sqlite3.connect(
    "data/dot_ai.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS memory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    key TEXT,
    value TEXT
)
""")

conn.commit()