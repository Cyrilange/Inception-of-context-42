import ast
import hashlib
from pathlib import Path

from .config import LANGUAGES
from .models import Chunk


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


def get_chunk_id( relative_path: str, symbol: str, chunk_type: str) -> str:
    """
    Return a stable identifier for a code chunk.
    """
    identity = f"{relative_path}::{chunk_type}::{symbol}"
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()

def build_chunk( path: Path, relative_path: str, source: str, node: ast.AST ) -> Chunk:
    """
    Build a Chunk object from an AST node.
    """
    name, start_line, end_line = get_node_info(node)
    content = get_node_content(source, node)
    chunk_type = get_chunk_type(node)
    content_hash = get_content_hash(content)
    language = get_language(path)
    chunk_id = get_chunk_id(relative_path, name, chunk_type)

    return Chunk(
        id=chunk_id,
        path=relative_path,
        language=language,
        chunk_type=chunk_type,
        symbol=name,
        start_line=start_line,
        end_line=end_line,
        content_hash=content_hash,
        content=content,
    )


def get_language(path: Path) -> str:
    """
    Return the language or format based on the file extension.
    """
    return LANGUAGES.get(path.suffix.lower(), "unknown")



#test 


def print_chunk(chunk: Chunk) -> None:
    """
    Print a chunk for debugging purposes.
    """
    print("----- CHUNK -----")
    print(f"ID: {chunk.id}")
    print(f"Path: {chunk.path}")
    print(f"Language: {chunk.language}")
    print(f"Type: {chunk.chunk_type}")
    print(f"Symbol: {chunk.symbol}")
    print(f"Lines: {chunk.start_line}-{chunk.end_line}")
    print(f"Hash: {chunk.content_hash}")
    print("Content:")
    print(chunk.content)

def main() -> None:
    source = """
def add(a, b):
    return a + b
    



class Calculator:
    def multiply(self, a, b):
        return a * b
"""

    path = Path("calculator.py")
    relative_path = "calculator.py"

    tree = parse_python(source)
    definitions = find_definitions(tree)

    for node in definitions:
        chunk = build_chunk(
            path=path,
            relative_path=relative_path,
            source=source,
            node=node,
        )

        print_chunk(chunk)


if __name__ == "__main__":
    main()