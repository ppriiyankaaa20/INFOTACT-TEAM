import sys
import time
import os

from database import DatabaseManager
from config import (
    IGNORE_VARIABLES,
    TRACE_LINE,
    TRACE_CALL,
    TRACE_RETURN,
    TRACE_EXCEPTION,
    MAX_HISTORY,
    DEBUG
)


class ExecutionTracer:

    def __init__(self):

        self.database = DatabaseManager()

        self.execution_history = []

        self.start_time = None

        self.frame_count = 0

        self.enabled = False

    def start(self):

        self.execution_history.clear()

        self.frame_count = 0

        self.start_time = time.time()

        self.enabled = True

        sys.settrace(self.trace)

    # ---------------------------------------------------------

    def stop(self):

        sys.settrace(None)

        self.enabled = False

        self.database.close()

    # ---------------------------------------------------------

    def trace(self, frame, event, arg):

        if not self.enabled:
            return

        filename = os.path.basename(frame.f_code.co_filename)

        # Ignore library files
        if filename != "sample.py":
            return self.trace

        # Ignore unwanted events
        if event == "line" and not TRACE_LINE:
            return self.trace

        if event == "call" and not TRACE_CALL:
            return self.trace

        if event == "return" and not TRACE_RETURN:
            return self.trace

        if event == "exception" and not TRACE_EXCEPTION:
            return self.trace

        self.frame_count += 1

        line_number = frame.f_lineno

        function_name = frame.f_code.co_name

        variables = {}

        for key, value in frame.f_locals.items():

            if key in IGNORE_VARIABLES:
                continue

            variables[key] = repr(value)

        record = {

            "event": event,

            "line": line_number,

            "function": function_name,

            "variables": variables

        }

        if len(self.execution_history) < MAX_HISTORY:

            self.execution_history.append(record)

        # Save into database

        self.database.save_execution(

            filename,

            function_name,

            line_number,

            variables

        )

        if DEBUG:

            print("=" * 60)

            print(f"Event      : {event}")

            print(f"Line       : {line_number}")

            print(f"Function   : {function_name}")

            if len(variables) == 0:

                print("Variables  : None")

            else:

                print("Variables")

                for key, value in variables.items():

                    print(f"   {key} = {value}")

        return self.trace

    # ---------------------------------------------------------

    def get_history(self):

        return self.execution_history

    # ---------------------------------------------------------

    def clear(self):

        self.execution_history.clear()

        self.frame_count = 0

    # ---------------------------------------------------------

    def summary(self):

        elapsed = time.time() - self.start_time

        print("\n")

        print("=" * 60)

        print("Execution Summary")

        print("=" * 60)

        print(f"Frames Recorded : {self.frame_count}")

        print(f"Execution Time  : {elapsed:.4f} sec")

        print(f"History Objects : {len(self.execution_history)}")

        print("=" * 60)