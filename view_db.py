import sqlite3

connection = sqlite3.connect("trace.db")
cursor = connection.cursor()


cursor.execute("SELECT * FROM variable_history")

for row in cursor.fetchall():
    print(row)

connection.close()