import ast
import hashlib
from pathlib import Path


def parse_python(source: str) -> ast.AST:
    """
    Parse Python source code into an abstract syntax tree (AST).
    """
    return ast.parse(source)


def find_definitions(tree: ast.AST) -> list[ast.AST]:
    """
    Find functions, async functions, and classes in the AST.
    """
    return [
        node
        for node in ast.walk(tree)
        if isinstance(
            node,
            (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef),
        )
    ]

def get_node_info(node: ast.AST) -> tuple[str, int, int]:
    """
    Return the symbol name and source line range of an AST node.
    """
    name = getattr(node, "name", "<anonymous>")
    start_line = node.lineno
    end_line = node.end_lineno

    return name, start_line, end_line

def get_node_content(source: str, node: ast.AST) -> str:
    """
    Return the source code corresponding to an AST node.
    """
    content = ast.get_source_segment(source, node)

    if content is None:
        return ""

    return content

def get_chunk_type(node: ast.AST) -> str:
    """
    Return the IoC chunk type for an AST node.
    """
    if isinstance(node, ast.ClassDef):
        return "class"

    if isinstance(node, ast.AsyncFunctionDef):
        return "async_function"

    if isinstance(node, ast.FunctionDef):
        return "function"

    return "unknown"

def get_content_hash(content: str) -> str:
    """
    Return a SHA-256 hash of the chunk content.
    """
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def get_language(path: Path) -> str:
    """
    Return the programming language based on the file extension.
    """
    extension = path.suffix.lower()

    if extension == ".py":
        return "python"

    return "unknown"