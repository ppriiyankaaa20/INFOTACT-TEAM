import sqlite3

with sqlite3.connect("trace.db") as connection:
    for row in connection.execute("SELECT * FROM variable_history"):
        print(row)
