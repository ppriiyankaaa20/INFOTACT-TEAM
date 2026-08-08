import json
import sqlite3

from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer, Static, Button, Input


def deserialize_value(value):
    """Convert stored JSON value back to Python value."""

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

        # Current execution step
        self.current = 0

        # All execution records
        self.records = []

        # Variable selected for watching
        self.watch_variable = None

        # History of watched variable
        self.watch_records = []

        # Code shown in UI
        self.code_lines = [
            "x = 10",
            "y = 20",
            "z = x + y",
            "z += 5",
            "print(z)"
        ]

    # ---------------------------------------------------------
    # LOAD EXECUTION HISTORY
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # LOAD WATCH VARIABLE
    # ---------------------------------------------------------

    def load_watch_variable(self):

        self.watch_records = []

        if not self.watch_variable:
            return

        conn = sqlite3.connect("history.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT line_number,
                   variable_name,
                   serialized_value
            FROM execution_history
            WHERE variable_name = ?
            ORDER BY id
        """, (self.watch_variable,))

        self.watch_records = cursor.fetchall()

        conn.close()

    # ---------------------------------------------------------
    # UI COMPONENTS
    # ---------------------------------------------------------

    def compose(self) -> ComposeResult:

        self.load_execution()

        yield Header(show_clock=True)

        # Code View
        yield Static(
            "",
            id="code"
        )

        # Previous / Next controls
        yield Horizontal(
            Button("Previous", id="prev"),
            Button("Next", id="next"),
            Static("", id="step")
        )

        # Execution Timeline
        yield Static(
            "",
            id="timeline"
        )

        # Watch Variable Input + Button
        yield Horizontal(
            Input(
                placeholder="Enter variable name (e.g. z)",
                id="watch_input"
            ),
            Button(
                "Watch",
                id="watch_btn"
            )
        )

        # Watch Variables Panel
        yield Static(
            "WATCH VARIABLES\n\n"
            "No variable selected.",
            id="watch_panel"
        )

        yield Footer()

    # ---------------------------------------------------------
    # WHEN APP STARTS
    # ---------------------------------------------------------

    def on_mount(self):

        self.update_screen()

    # ---------------------------------------------------------
    # UPDATE CODE + TIMELINE
    # ---------------------------------------------------------

    def update_screen(self):

        code = ""

        highlight = None

        # Find current execution line
        if self.records:
            highlight = self.records[self.current][0]

        # Build code view
        for i, line in enumerate(self.code_lines, start=1):

            if i == highlight:
                code += f">>> {line}\n"
            else:
                code += f"    {line}\n"

        self.query_one("#code", Static).update(
            "CODE VIEW\n\n" + code
        )

        # -----------------------------------------------------
        # EXECUTION TIMELINE
        # -----------------------------------------------------

        if self.records:

            line, variable, value = self.records[self.current]

            value = deserialize_value(value)

            timeline = (
                f"Line     : {line}\n"
                f"Variable : {variable}\n"
                f"Value    : {value}"
            )

        else:

            timeline = "No execution history found."

        self.query_one("#timeline", Static).update(
            "EXECUTION TIMELINE\n\n" + timeline
        )

        # -----------------------------------------------------
        # STEP COUNTER
        # -----------------------------------------------------

        if self.records:

            self.query_one("#step", Static).update(
                f"Step {self.current + 1}/{len(self.records)}"
            )

        else:

            self.query_one("#step", Static).update(
                "Step 0/0"
            )

        # Update Watch Variables
        self.update_watch()

    # ---------------------------------------------------------
    # WATCH VARIABLES DISPLAY
    # ---------------------------------------------------------

    def update_watch(self):

        # No variable selected
        if not self.watch_variable:

            self.query_one(
                "#watch_panel",
                Static
            ).update(
                "WATCH VARIABLES\n\n"
                "No variable selected."
            )

            return

        text = (
            "WATCH VARIABLES\n\n"
            f"Variable : {self.watch_variable}\n"
            "----------------------------------------\n"
        )

        # No records for selected variable
        if not self.watch_records:

            text += "No history found."

        else:

            # Display every value of watched variable
            for line, variable, value in self.watch_records:

                value = deserialize_value(value)

                text += (
                    f"Line {line}  →  {value}\n"
                )

        self.query_one(
            "#watch_panel",
            Static
        ).update(text)

    # ---------------------------------------------------------
    # BUTTON EVENTS
    # ---------------------------------------------------------

    def on_button_pressed(self, event: Button.Pressed):

        # -----------------------------------------------------
        # WATCH BUTTON
        # -----------------------------------------------------

        if event.button.id == "watch_btn":

            variable = self.query_one(
                "#watch_input",
                Input
            ).value.strip()

            if variable:

                self.watch_variable = variable

                # Load selected variable history
                self.load_watch_variable()

                # Display history
                self.update_watch()

            return

        # -----------------------------------------------------
        # IF THERE IS NO EXECUTION DATA
        # -----------------------------------------------------

        if not self.records:
            return

        # -----------------------------------------------------
        # NEXT BUTTON
        # -----------------------------------------------------

        if event.button.id == "next":

            if self.current < len(self.records) - 1:
                self.current += 1

        # -----------------------------------------------------
        # PREVIOUS BUTTON
        # -----------------------------------------------------

        elif event.button.id == "prev":

            if self.current > 0:
                self.current -= 1

        # Refresh UI
        self.update_screen()


# -------------------------------------------------------------
# START APPLICATION
# -------------------------------------------------------------

if __name__ == "__main__":
    PyChronicle().run()