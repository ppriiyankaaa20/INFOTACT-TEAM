import ast
import sqlite3
from datetime import datetime

# Connect to SQLite database
connection = sqlite3.connect("trace.db")
cursor = connection.cursor()

# Clear old records (Optional)
cursor.execute("DELETE FROM variable_history")

def parse_file(filename):

    # Read target Python file
    with open(filename, "r") as file:
        source = file.read()

    # Convert source code into AST
    tree = ast.parse(source)

    # Traverse all AST nodes
    for node in ast.walk(tree):

        # Check for assignment statements
        if isinstance(node, ast.Assign):

            # Handle multiple assignment targets
            for target in node.targets:

                if isinstance(target, ast.Name):

                    variable_name = target.id
                    line_number = node.lineno

                    print("Variable :", variable_name)
                    print("Line :", line_number)

                    # Save into database
                    cursor.execute("""
                        INSERT INTO variable_history
                        (timestamp, line_number, variable_name, serialized_value)
                        VALUES (?, ?, ?, ?)
                    """, (
                        datetime.now().isoformat(),
                        line_number,
                        variable_name,
                        None
                    ))

    connection.commit()
    connection.close()
    print("Variables Saved Successfully")

# Call the function
# parse_file("sample.py")

