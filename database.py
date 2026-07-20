import sqlite3

connection = sqlite3.connect("trace.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS variable_history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    line_number INTEGER,
    variable_name TEXT,
    serialized_value TEXT
)
""")

connection.commit()
connection.close()

print("Database Ready")