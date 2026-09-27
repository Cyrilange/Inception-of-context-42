from pathlib import Path

from .config import (
    IGNORED_DIRECTORIES,
    MAX_FILE_SIZE_BYTES,
    is_supported_file,
)


def is_binary_file(path: Path) -> bool:
    """
    Return True if the file looks like a binary file.
    """
    try:
        with path.open("rb") as file:
            chunk = file.read(4096)
    except OSError:
        return True

    return b"\x00" in chunk


def discover_files( target: Path,  excluded_paths: set[Path] | None = None,) -> list[Path]:
    """
    Recursively discover source files that are allowed to be indexed.
    """

    target = target.resolve()

    if not target.exists(): 
        raise FileNotFoundError(f"Target directory does not exist: {target}")

    if not target.is_dir():
        raise NotADirectoryError(f"Target is not a directory: {target}")

    excluded = {
        path.resolve()
        for path in (excluded_paths or set())
    }

    discovered: list[Path] = []

    for current_path, directories, filenames in target.walk():

        directories[:] = [
            directory
            for directory in directories
            if not directory.startswith(".")
            and directory not in IGNORED_DIRECTORIES
            and not any(
                (current_path / directory).resolve().is_relative_to( excluded_path)
                for excluded_path in excluded 
                )
        ]

        for filename in filenames:
            path = current_path / filename

            if path.name.startswith("."):
                continue

            if not is_supported_file(path):
                continue

            try:
                if path.stat().st_size > MAX_FILE_SIZE_BYTES:
                    continue
            except OSError:
                continue

            if is_binary_file(path):
                continue

            if excluded and any(
                path.is_relative_to(excluded_path)
                for excluded_path in excluded
            ):
                continue

            discovered.append(path)

    return sorted(discovered)

