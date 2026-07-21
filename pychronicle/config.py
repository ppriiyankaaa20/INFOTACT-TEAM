"""Runtime configuration for PyChronicle."""

BANNER = "PyChronicle - Python Execution History"
LINE = "=" * 60

# These paths are relative to the pychronicle directory when running main.py.
DATABASE_PATH = "history.db"
TARGET_FILE = "sample.py"

# Execution tracer options.
IGNORE_VARIABLES = {"__builtins__"}
TRACE_LINE = True
TRACE_CALL = True
TRACE_RETURN = True
TRACE_EXCEPTION = True
MAX_HISTORY = 1_000
DEBUG = False
