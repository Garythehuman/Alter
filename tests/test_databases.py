"""Tests for database detection."""

import tempfile
from pathlib import Path

from alter.detectors.databases import detect


def _make_tree(files: dict[str, str]) -> str:
    tmpdir = tempfile.mkdtemp()
    for rel_path, content in files.items():
        full = Path(tmpdir) / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
    return tmpdir


def test_detects_postgres_from_env():
    d = _make_tree({".env": "DATABASE_URL=postgresql://user:pass@localhost/mydb\n"})
    result = detect(d)
    dbs = [r["database"] for r in result]
    assert "PostgreSQL" in dbs


def test_detects_mongodb_from_env():
    d = _make_tree({".env.example": "MONGO_URI=mongodb://localhost:27017/mydb\n"})
    result = detect(d)
    dbs = [r["database"] for r in result]
    assert "MongoDB" in dbs


def test_detects_redis_from_env():
    d = _make_tree({".env": "REDIS_URL=redis://localhost:6379\n"})
    result = detect(d)
    dbs = [r["database"] for r in result]
    assert "Redis" in dbs


def test_detects_psycopg2_from_requirements():
    d = _make_tree({"requirements.txt": "psycopg2==2.9.9\ndjango==4.2\n"})
    result = detect(d)
    dbs = [r["database"] for r in result]
    assert "PostgreSQL" in dbs


def test_detects_pymongo_from_requirements():
    d = _make_tree({"requirements.txt": "pymongo==4.6\n"})
    result = detect(d)
    dbs = [r["database"] for r in result]
    assert "MongoDB" in dbs


def test_no_duplicates():
    # Both .env and requirements.txt mention Postgres — should appear once
    d = _make_tree({
        ".env": "DATABASE_URL=postgresql://localhost/db\n",
        "requirements.txt": "psycopg2==2.9\n",
    })
    result = detect(d)
    pg_entries = [r for r in result if r["database"] == "PostgreSQL"]
    assert len(pg_entries) == 1


def test_empty_directory():
    d = _make_tree({})
    assert detect(d) == []
