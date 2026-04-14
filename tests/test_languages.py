"""Tests for language detection."""

import os
import tempfile
from pathlib import Path

from alter.detectors.languages import detect


def _make_tree(files: dict[str, str]) -> str:
    """Create a temp directory with the given file structure and return its path."""
    tmpdir = tempfile.mkdtemp()
    for rel_path, content in files.items():
        full = Path(tmpdir) / rel_path
        full.parent.mkdir(parents=True, exist_ok=True)
        full.write_text(content)
    return tmpdir


def test_detects_python():
    d = _make_tree({"main.py": "", "utils.py": "", "README.md": ""})
    result = detect(d)
    langs = [r["language"] for r in result]
    assert "Python" in langs


def test_detects_multiple_languages():
    d = _make_tree({"app.py": "", "index.js": "", "style.css": ""})
    result = detect(d)
    langs = [r["language"] for r in result]
    assert "Python" in langs
    assert "JavaScript" in langs
    assert "CSS" in langs


def test_sorted_by_file_count():
    d = _make_tree({"a.py": "", "b.py": "", "c.py": "", "index.js": ""})
    result = detect(d)
    assert result[0]["language"] == "Python"
    assert result[0]["files"] == 3


def test_skips_node_modules():
    d = _make_tree({"src/app.py": "", "node_modules/lib/index.js": ""})
    result = detect(d)
    langs = [r["language"] for r in result]
    assert "Python" in langs
    # JavaScript from node_modules should be ignored
    assert "JavaScript" not in langs


def test_empty_directory():
    d = _make_tree({})
    assert detect(d) == []


def test_unknown_extensions_ignored():
    d = _make_tree({"file.xyz": "", "data.bin": ""})
    assert detect(d) == []
