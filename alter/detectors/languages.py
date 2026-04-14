"""Detect programming languages in a project directory by file extension."""

from pathlib import Path

# Maps file extension -> language name
EXTENSION_MAP: dict[str, str] = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".jsx": "JavaScript",
    ".tsx": "TypeScript",
    ".rb": "Ruby",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".cs": "C#",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".cpp": "C++",
    ".cc": "C++",
    ".c": "C",
    ".h": "C/C++",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",
    ".lua": "Lua",
    ".ex": "Elixir",
    ".exs": "Elixir",
    ".hs": "Haskell",
    ".r": "R",
    ".R": "R",
    ".sql": "SQL",
    ".dart": "Dart",
}

# Directories to skip during scanning
IGNORED_DIRS = {
    ".git", ".hg", ".svn",
    "node_modules", ".venv", "venv", "env", "__pycache__",
    ".mypy_cache", ".pytest_cache", "dist", "build", "target",
    ".next", ".nuxt", "out",
}


def detect(path: str) -> list[dict]:
    """Scan a directory and return detected languages with file counts.

    Args:
        path: Root directory to scan.

    Returns:
        List of dicts sorted by file count descending:
        [{"language": "Python", "files": 12}, ...]
    """
    counts: dict[str, int] = {}
    root = Path(path).resolve()

    for file in root.rglob("*"):
        if not file.is_file():
            continue
        # Skip ignored directories
        if any(part in IGNORED_DIRS for part in file.parts):
            continue
        lang = EXTENSION_MAP.get(file.suffix.lower())
        if lang:
            counts[lang] = counts.get(lang, 0) + 1

    return [
        {"language": lang, "files": count}
        for lang, count in sorted(counts.items(), key=lambda x: -x[1])
    ]
