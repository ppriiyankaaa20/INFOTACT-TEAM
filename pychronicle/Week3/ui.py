import json
import sqlite3

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, Button


def deserialize_value(value):
    if value is None:
        return None

    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value


class PyChronicle(App):

    CSS_PATH = "ui.tcss"
    TITLE = "PyChronicle"

    def __init__(self):
        super().__init__()

        self.current = 0
        self.records = []

        self.code_lines = [
            "x = 10",
            "y = 20",
            "z = x + y",
            "z += 5",
            "print(z)"
        ]
        
    def load_execution(self):

        conn = sqlite3.connect("history.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT line_number,
               variable_name,
               serialized_value
        FROM execution_history
        ORDER BY id
        """)
        
        self.records = cursor.fetchall()
        
        conn.close()

    def compose(self) -> ComposeResult:

        self.load_execution()

        yield Header(show_clock=True)

        yield Static("", id="code")

        yield Horizontal(
            Button("Previous", id="prev"),
            Button("Next", id="next"),
            Static("", id="step")
        )

        yield Static("", id="timeline")

        yield Footer()

    def on_mount(self):

        self.update_screen()

    def update_screen(self):

        code = ""

        highlight = None

        if self.records:
           highlight = self.records[self.current][0]

        for i, line in enumerate(self.code_lines, start=1):

           if i == highlight:
            code += f">>> {line}\n"
           else:
            code += f"    {line}\n"

        self.query_one("#code", Static).update(
        "CODE VIEW\n\n" + code
    )

        timeline = ""

        if self.records:

          line, variable, value = self.records[self.current]

          timeline = (
            f"Line     : {line}\n"
            f"Variable : {variable}\n"
            f"Value    : {deserialize_value(value)}"
        )
        # timeline =self.records[self.current]
        # print(timeline)

        self.query_one("#timeline", Static).update(
        "EXECUTION TIMELINE\n\n" + timeline
    )

        self.query_one("#step", Static).update(
        f"Step {self.current + 1}/{len(self.records)}"
    )
    def on_button_pressed(self, event: Button.Pressed):

        if not self.records:
            return

        if event.button.id == "next":

            if self.current < len(self.records)-1:
                self.current += 1

        elif event.button.id == "prev":

            if self.current > 0:
                self.current -= 1

        self.update_screen()
       

if __name__ == "__main__":
    PyChronicle().run()