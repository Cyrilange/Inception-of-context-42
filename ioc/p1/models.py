from dataclasses import dataclass


@dataclass(frozen=True)
class Chunk:
    id: str
    path: str
    language: str
    chunk_type: str
    symbol: str | None
    start_line: int
    end_line: int
    content_hash: str
    content: str