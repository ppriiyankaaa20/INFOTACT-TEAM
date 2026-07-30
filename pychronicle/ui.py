from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
import sqlite3

class PyChronicle(App):
    CSS_PATH="ui.tcss"
    TITLE="PyChronicle"

    def get_execution(self):
        conn = sqlite3.connect("history.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT timestamp,
               line_number,
               variable_name,
               serialized_value
        FROM execution_history
        LIMIT 15
        """)

        rows = cursor.fetchall()

        text = ""

        for timestamp, line, variable, value in rows:
            text += f"{timestamp} | Line {line} | {variable} = {value}\n"

        return text
        conn.close()

        output = "Execution Timeline\n\n"

        if not rows:
            output += "No execution data found."
        else:
            for line, var, value in rows:
                output += f"Line {line} | {var} = {value}\n"

        return output

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        code = (
            "Code View\n\n"
            "x = 10\n"
            "y = 20\n"
            "z = x + y\n"
            "print(z)"
        )

        yield Static(
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "        CODE VIEW\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    + code,
    id="code"
)

        yield Static(
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    "   EXECUTION TIMELINE\n"
    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    + self.get_execution(),
    id="timeline"
)

        yield Footer()


if __name__ == "__main__":
    PyChronicle().run()