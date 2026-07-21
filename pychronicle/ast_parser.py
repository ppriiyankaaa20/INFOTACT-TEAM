import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Assignment:
    """One variable assignment discovered in a Python source file."""

    name: str
    line_number: int
    assignment_type: str


class VariableVisitor(ast.NodeVisitor):

    def __init__(self):
        self.assignments: list[Assignment] = []

    def visit_Assign(self, node):
        self._record_targets(node.targets, node.lineno, "assignment")
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self._record_targets([node.target], node.lineno, "annotated assignment")
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        self._record_targets([node.target], node.lineno, "augmented assignment")
        self.generic_visit(node)

    def visit_NamedExpr(self, node):
        self._record_targets([node.target], node.lineno, "named expression")
        self.generic_visit(node)

    def _record_targets(self, targets: Iterable[ast.expr], line_number: int, assignment_type: str):
        for target in targets:
            for name in self._names_in_target(target):
                self.assignments.append(Assignment(name, line_number, assignment_type))

    @staticmethod
    def _names_in_target(target: ast.expr) -> Iterable[str]:
        if isinstance(target, ast.Name):
            yield target.id
        elif isinstance(target, (ast.Tuple, ast.List)):
            for element in target.elts:
                yield from VariableVisitor._names_in_target(element)


class ASTParser:

    def __init__(self, filename):

        self.filename = Path(filename)
        self.source_code = ""
        self.tree = None

    def load_file(self):

        with self.filename.open("r", encoding="utf-8") as file:
            self.source_code = file.read()

        print("\nSource File Loaded Successfully\n")

    def parse_ast(self):

        self.tree = ast.parse(self.source_code, filename=str(self.filename))

        print("AST Generated Successfully\n")

    def find_assignments(self):

        print("Searching Variable Assignments...\n")

        if self.tree is None:
            raise RuntimeError("Parse the source file before searching for assignments.")

        visitor = VariableVisitor()
        visitor.visit(self.tree)

        for assignment in visitor.assignments:
            print("-" * 50)
            print(f"Variable Name : {assignment.name}")
            print(f"Line Number   : {assignment.line_number}")
            print(f"Type          : {assignment.assignment_type}")

        print(f"\nAssignments Found: {len(visitor.assignments)}\n")
        return visitor.assignments
