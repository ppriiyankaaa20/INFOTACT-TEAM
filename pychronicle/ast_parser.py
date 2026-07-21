import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Assignment:
    name: str
    line_number: int
    assignment_type: str


class VariableVisitor(ast.NodeVisitor):
    ASSIGNMENT_TYPES = {
        ast.Assign: "assignment",
        ast.AnnAssign: "annotated assignment",
        ast.AugAssign: "augmented assignment",
        ast.NamedExpr: "named expression",
    }

    def __init__(self):
        self.assignments: list[Assignment] = []

    def visit(self, node):
        assignment_type = self.ASSIGNMENT_TYPES.get(type(node))
        if assignment_type:
            targets = node.targets if hasattr(node, "targets") else [node.target]
            self._record(targets, node.lineno, assignment_type)
        return super().visit(node)

    def _record(self, targets: Iterable[ast.expr], line_number: int, assignment_type: str):
        for target in targets:
            for name in self._names(target):
                self.assignments.append(Assignment(name, line_number, assignment_type))

    @classmethod
    def _names(cls, target: ast.expr) -> Iterable[str]:
        if isinstance(target, ast.Name):
            yield target.id
        elif isinstance(target, (ast.Tuple, ast.List)):
            for item in target.elts:
                yield from cls._names(item)


class ASTParser:
    def __init__(self, filename):
        self.filename, self.source_code, self.tree = Path(filename), "", None

    def load_file(self):
        self.source_code = self.filename.read_text(encoding="utf-8")
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
        for item in visitor.assignments:
            print("-" * 50)
            print(f"Variable Name : {item.name}")
            print(f"Line Number   : {item.line_number}")
            print(f"Type          : {item.assignment_type}")
        print(f"\nAssignments Found: {len(visitor.assignments)}\n")
        return visitor.assignments
