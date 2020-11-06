import ast
import sys
from typing import Any, Type, Tuple, Generator, List

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

FS101 = 'FS101 String formatting has callable object'


class Visitor(ast.NodeVisitor):
    def __init__(self):
        self.errors: List[Tuple[int, int, str]] = []

    def visit_JoinedStr(self, node: ast.Call):
        for value in node.values:
            if hasattr(value, 'value') and isinstance(value.value, ast.Call):
                self.errors.append((node.lineno, node.col_offset, FS101))
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST) -> None:
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
