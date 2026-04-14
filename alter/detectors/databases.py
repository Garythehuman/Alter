"""Detect databases referenced in a project's config and dependency files."""

import json
import re
from pathlib import Path

import yaml


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _read_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


# Maps keyword pattern -> database label
DEPENDENCY_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bpsycopg2\b|\bpsycopg\b|\basyncpg\b"), "PostgreSQL"),
    (re.compile(r"\bpymysql\b|\bmysql-connector\b|\baiomysql\b"), "MySQL"),
    (re.compile(r"\bsqlite3\b|\baiosqlite\b"), "SQLite"),
    (re.compile(r"\bpymongo\b|\bmotor\b"), "MongoDB"),
    (re.compile(r"\bredis\b|\baioredis\b"), "Redis"),
    (re.compile(r"\belasticsearch\b"), "Elasticsearch"),
    (re.compile(r"\bcassandra-driver\b"), "Cassandra"),
    (re.compile(r"\bpg\b|\"pg\""), "PostgreSQL"),
    (re.compile(r"\bmysql2\b|\"mysql2\""), "MySQL"),
    (re.compile(r"\bmongoose\b|\"mongoose\""), "MongoDB"),
    (re.compile(r"\bioredis\b|\"ioredis\""), "Redis"),
    (re.compile(r"\bsqlite3\b|\"sqlite3\""), "SQLite"),
    (re.compile(r"\bsequelize\b"), "SQL (Sequelize)"),
    (re.compile(r"\bprisma\b"), "SQL (Prisma)"),
    (re.compile(r"\btypeorm\b"), "SQL (TypeORM)"),
]

# Connection string URL scheme -> database label
URL_SCHEME_MAP: dict[str, str] = {
    "postgres://": "PostgreSQL",
    "postgresql://": "PostgreSQL",
    "mysql://": "MySQL",
    "mongodb://": "MongoDB",
    "mongodb+srv://": "MongoDB",
    "redis://": "Redis",
    "rediss://": "Redis",
    "sqlite:///": "SQLite",
}

ENV_FILES = [".env", ".env.example", ".env.sample", ".env.local"]
CONFIG_FILES = ["database.yml", "database.yaml", "config/database.yml"]
DEP_FILES = ["requirements.txt", "Pipfile", "package.json", "pyproject.toml", "Gemfile", "go.mod"]


def _scan_for_urls(text: str) -> list[str]:
    found = []
    for scheme, label in URL_SCHEME_MAP.items():
        if scheme in text and label not in found:
            found.append(label)
    return found


def _scan_for_deps(text: str) -> list[str]:
    found = []
    for pattern, label in DEPENDENCY_PATTERNS:
        if pattern.search(text) and label not in found:
            found.append(label)
    return found


def detect(path: str) -> list[dict]:
    """Detect databases referenced in config files and dependencies.

    Args:
        path: Root directory to scan.

    Returns:
        List of dicts: [{"database": "PostgreSQL", "source": ".env"}, ...]
    """
    root = Path(path).resolve()
    results: list[dict] = []
    seen: set[str] = set()

    def add(label: str, source: str) -> None:
        if label not in seen:
            seen.add(label)
            results.append({"database": label, "source": source})

    # Scan env files for connection strings
    for name in ENV_FILES:
        f = root / name
        if f.exists():
            for label in _scan_for_urls(_read_text(f)):
                add(label, name)

    # Scan YAML database config files
    for name in CONFIG_FILES:
        f = root / name
        if f.exists():
            text = _read_text(f)
            for label in _scan_for_urls(text):
                add(label, name)
            data = _read_yaml(f)
            adapter = str(data.get("default", {}).get("adapter", ""))
            if "postgresql" in adapter or "postgres" in adapter:
                add("PostgreSQL", name)
            elif "mysql" in adapter:
                add("MySQL", name)
            elif "sqlite" in adapter:
                add("SQLite", name)

    # Scan dependency files for database packages
    for name in DEP_FILES:
        f = root / name
        if f.exists():
            for label in _scan_for_deps(_read_text(f)):
                add(label, name)

    return results
