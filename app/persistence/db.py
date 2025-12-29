# SQLite connection
import sqlite3

from app.config import DB_NAME


class Database:
    _connection = None

    @classmethod
    def connect(cls):
        if cls._connection is None:
            cls._connection = sqlite3.connect(DB_NAME, check_same_thread=False)
            cls._connection.row_factory = sqlite3.Row
        return cls._connection

    @classmethod
    def init(cls):
        conn = cls.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS sessions (
            date TEXT PRIMARY KEY,
            answered_count INTEGER NOT NULL,
            completed INTEGER NOT NULL
        )
        """
        )

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT,
            question TEXT,
            user_answer TEXT,
            correct_answer TEXT,
            is_correct INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        conn.commit()
