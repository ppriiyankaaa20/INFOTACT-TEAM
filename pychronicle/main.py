import argparse
import traceback

from ast_parser import ASTParser
from config import BANNER, DATABASE_PATH, LINE, TARGET_FILE
from database import DatabaseManager


class PyChronicle:
    """Week 1 foundation: static AST analysis and SQLite schema setup."""

    def __init__(self, target_file=TARGET_FILE):
        self.parser = ASTParser(target_file)
        self.database = DatabaseManager(DATABASE_PATH)

    def ast_phase(self):
        print(LINE)
        print("STEP 1 : AST ANALYSIS")
        print(LINE)
        self.parser.load_file()
        self.parser.parse_ast()
        return self.parser.find_assignments()

    def storage_phase(self):
        print(LINE)
        print("STEP 2 : SQLITE STORAGE SCHEMA")
        print(LINE)
        print(f"Database ready: {DATABASE_PATH}")
        print("Columns: timestamp, line_number, variable_name, serialized_value")

    def run(self):
        print(BANNER)
        self.ast_phase()
        self.storage_phase()

    def close(self):
        self.database.close()


def main():
    argument_parser = argparse.ArgumentParser(
        description="PyChronicle Week 1: find Python variable assignments with AST."
    )
    argument_parser.add_argument(
        "target_file",
        nargs="?",
        default=TARGET_FILE,
        help="Python file to analyse (default: sample.py).",
    )
    arguments = argument_parser.parse_args()
    app = None

    try:
        app = PyChronicle(arguments.target_file)
        app.run()
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
    except Exception:
        print("\nApplication error\n")
        traceback.print_exc()
    finally:
        if app is not None:
            app.close()


if __name__ == "__main__":
    main()
