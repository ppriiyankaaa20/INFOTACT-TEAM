import sqlite3

conn = sqlite3.connect("history.db")
cursor = conn.cursor()

cursor.execute("""
SELECT timestamp,
       line_number,
       variable_name,
       serialized_value
FROM execution_history
""")

rows = cursor.fetchall()

print("Execution History")
print("-----------------")

print("\nExecution History")
print("-" * 70)

for timestamp, line, variable, value in rows[:15]:
    print(f"Time     : {timestamp}")
    print(f"Line     : {line}")
    print(f"Variable : {variable}")
    print(f"Value    : {value}")
    print("-" * 70)

conn.close()