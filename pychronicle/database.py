import json
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_name="history.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS execution_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                line_number INTEGER NOT NULL,
                variable_name TEXT NOT NULL,
                serialized_value TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def save_variable_state(self, line_number, variable_name, value):
        self.cursor.execute(
            """
            INSERT INTO execution_history
                (timestamp, line_number, variable_name, serialized_value)
            VALUES (?, ?, ?, ?)
            """,
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), line_number,
             variable_name, json.dumps(value, default=str)),
        )
        self.connection.commit()

    def get_all_history(self):
        return self.cursor.execute("SELECT * FROM execution_history ORDER BY id").fetchall()

    def clear_history(self):
        self.cursor.execute("DELETE FROM execution_history")
        self.connection.commit()

    def close(self):
        self.connection.close()
