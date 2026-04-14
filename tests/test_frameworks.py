"""Tests for framework detection."""

import json
import tempfile
from pathlib import Path

from alter.detectors.frameworks import detect


def _make_tree(files: dict[str, str]) -> str:
    tmpdir = tempfile.mkdtemp()
    for rel_path, content in files.items():
        full = Path(tmpdir) / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
    return tmpdir


def test_detects_react_from_package_json():
    pkg = json.dumps({"dependencies": {"react": "^18.0.0", "react-dom": "^18.0.0"}})
    d = _make_tree({"package.json": pkg})
    result = detect(d)
    names = [r["framework"] for r in result]
    assert "React" in names


def test_detects_nextjs_from_package_json():
    pkg = json.dumps({"dependencies": {"next": "^14.0.0", "react": "^18.0.0"}})
    d = _make_tree({"package.json": pkg})
    result = detect(d)
    names = [r["framework"] for r in result]
    assert "Next.js" in names
    assert "React" in names


def test_detects_django_from_requirements():
    d = _make_tree({"requirements.txt": "django==4.2\npsycopg2==2.9\n"})
    result = detect(d)
    names = [r["framework"] for r in result]
    assert "Django" in names


def test_detects_fastapi_from_pyproject():
    toml = '[project]\ndependencies = ["fastapi>=0.110", "uvicorn"]\n'
    d = _make_tree({"pyproject.toml": toml})
    result = detect(d)
    names = [r["framework"] for r in result]
    assert "FastAPI" in names


def test_empty_directory():
    d = _make_tree({})
    assert detect(d) == []


def test_source_field_populated():
    pkg = json.dumps({"dependencies": {"express": "^4.0.0"}})
    d = _make_tree({"package.json": pkg})
    result = detect(d)
    assert result[0]["source"] == "package.json"
