# INFO TACT TEAM

## Description
A Python-based project for parsing Python source code and tracking variable assignments.

## Team Members
- Priyanka
- Devansh
- Jincy

           OutPut(ui.py)


━━━━━━━━━━━━━━━━━━━━━━━━━━
        CODE VIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━

Code View

x = 10
y = 20
z = x + y
print(z)
━━━━━━━━━━━━━━━━━━━━━━━━━━
   EXECUTION TIMELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━

2026-07-24 10:39:58 | Line 3 | x = "10"
2026-07-24 10:39:58 | Line 5 | x = "10"
2026-07-24 10:39:58 | Line 5 | y = "20"
2026-07-24 10:39:58 | Line 7 | x = "10"
2026-07-24 10:39:58 | Line 7 | y = "20"
2026-07-24 10:39:58 | Line 7 | z = "30"
2026-07-24 10:39:58 | Line 8 | x = "10"
2026-07-24 10:39:58 | Line 8 | y = "20"
2026-07-24 10:39:58 | Line 8 | z = "30"
2026-07-24 10:39:58 | Line 8 | i = "0"
2026-07-24 10:39:58 | Line 7 | x = "10"
2026-07-24 10:39:58 | Line 7 | y = "20"
2026-07-24 10:39:58 | Line 7 | z = "30"
2026-07-24 10:39:58 | Line 7 | i = "0"

Main.py

PyChronicle - Python Execution History
============================================================
STEP 1 : AST ANALYSIS
============================================================

Source File Loaded Successfully

AST Generated Successfully


Searching Variable Assignments...

--------------------------------------------------
Line Number    Variable Name    Type
--------------------------------------------------
1              x                assignment
3              y                assignment
5              z                assignment
8              z                augmented assignment
--------------------------------------------------
Assignments Found : 4
============================================================
STEP 2 : SQLITE STORAGE SCHEMA
============================================================
Database ready: history.db
Columns: timestamp, line_number, variable_name, serialized_value
40


============================================================
Execution Summary
============================================================
Frames Recorded : 17
Execution Time  : 2.0398 sec
History Objects : 71
============================================================
