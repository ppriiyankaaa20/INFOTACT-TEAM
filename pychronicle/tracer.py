import os
import sys
import time

from config import (
    DEBUG, IGNORE_VARIABLES, MAX_HISTORY, TRACE_CALL, TRACE_EXCEPTION,
    TRACE_LINE, TRACE_RETURN,
)
from database import DatabaseManager


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

    def stop(self):
        sys.settrace(None)
        self.enabled = False
        self.database.close()

    def trace(self, frame, event, arg):
        if not self.enabled:
            return

        filename = os.path.basename(frame.f_code.co_filename)
        ignored_event = (
            (event == "line" and not TRACE_LINE)
            or (event == "call" and not TRACE_CALL)
            or (event == "return" and not TRACE_RETURN)
            or (event == "exception" and not TRACE_EXCEPTION)
        )
        if filename != "sample.py" or ignored_event:
            return self.trace

        self.frame_count += 1
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name
        variables = {
            key: repr(value) for key, value in frame.f_locals.items()
            if key not in IGNORE_VARIABLES
        }
        record = {
            "event": event,
            "line": line_number,
            "function": function_name,
            "variables": variables,
        }
        if len(self.execution_history) < MAX_HISTORY:
            self.execution_history.append(record)

        self.database.save_execution(filename, function_name, line_number, variables)
        if DEBUG:
            self._print_event(event, line_number, function_name, variables)
        return self.trace

    @staticmethod
    def _print_event(event, line_number, function_name, variables):
        print("=" * 60)
        print(f"Event      : {event}")
        print(f"Line       : {line_number}")
        print(f"Function   : {function_name}")
        if not variables:
            print("Variables  : None")
            return
        print("Variables")
        for key, value in variables.items():
            print(f"   {key} = {value}")

    def get_history(self):
        return self.execution_history

    def clear(self):
        self.execution_history.clear()
        self.frame_count = 0

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
