"""Detect frameworks and libraries from project config files."""

import json
from pathlib import Path
from typing import Any

import yaml


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


def _read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return []


# Maps package name -> framework label
JS_FRAMEWORK_MAP: dict[str, str] = {
    "react": "React",
    "vue": "Vue.js",
    "svelte": "Svelte",
    "@angular/core": "Angular",
    "next": "Next.js",
    "nuxt": "Nuxt.js",
    "express": "Express",
    "fastify": "Fastify",
    "koa": "Koa",
    "nestjs": "NestJS",
    "electron": "Electron",
}

PYTHON_FRAMEWORK_MAP: dict[str, str] = {
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "tornado": "Tornado",
    "starlette": "Starlette",
    "aiohttp": "aiohttp",
    "typer": "Typer",
    "click": "Click",
    "streamlit": "Streamlit",
    "gradio": "Gradio",
    "celery": "Celery",
    "sqlalchemy": "SQLAlchemy",
    "pydantic": "Pydantic",
}

RUBY_FRAMEWORK_MAP: dict[str, str] = {
    "rails": "Ruby on Rails",
    "sinatra": "Sinatra",
    "hanami": "Hanami",
}

GO_FRAMEWORK_MAP: dict[str, str] = {
    "github.com/gin-gonic/gin": "Gin",
    "github.com/labstack/echo": "Echo",
    "github.com/gofiber/fiber": "Fiber",
    "github.com/go-chi/chi": "Chi",
}


def _from_package_json(root: Path) -> list[str]:
    pkg = _read_json(root / "package.json")
    deps = {
        **pkg.get("dependencies", {}),
        **pkg.get("devDependencies", {}),
    }
    return [
        JS_FRAMEWORK_MAP[name]
        for name in deps
        if name in JS_FRAMEWORK_MAP
    ]


def _from_requirements_txt(root: Path) -> list[str]:
    lines = _read_lines(root / "requirements.txt")
    found = []
    for line in lines:
        pkg = line.strip().split("==")[0].split(">=")[0].split("[")[0].lower()
        if pkg in PYTHON_FRAMEWORK_MAP:
            found.append(PYTHON_FRAMEWORK_MAP[pkg])
    return found


def _from_pyproject_toml(root: Path) -> list[str]:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

    try:
        data: Any = tomllib.loads((root / "pyproject.toml").read_bytes())  # type: ignore[arg-type]
    except Exception:
        return []

    deps = data.get("project", {}).get("dependencies", [])
    found = []
    for dep in deps:
        pkg = dep.split(">=")[0].split("==")[0].split("[")[0].lower().strip()
        if pkg in PYTHON_FRAMEWORK_MAP:
            found.append(PYTHON_FRAMEWORK_MAP[pkg])
    return found


def _from_gemfile(root: Path) -> list[str]:
    lines = _read_lines(root / "Gemfile")
    found = []
    for line in lines:
        line = line.strip()
        if line.startswith("gem "):
            parts = line.split()
            if len(parts) >= 2:
                name = parts[1].strip("'\",'")
                if name in RUBY_FRAMEWORK_MAP:
                    found.append(RUBY_FRAMEWORK_MAP[name])
    return found


def _from_go_mod(root: Path) -> list[str]:
    lines = _read_lines(root / "go.mod")
    found = []
    for line in lines:
        line = line.strip()
        for pkg, label in GO_FRAMEWORK_MAP.items():
            if line.startswith(pkg):
                found.append(label)
    return found


_DETECTORS = [
    ("package.json", _from_package_json),
    ("requirements.txt", _from_requirements_txt),
    ("pyproject.toml", _from_pyproject_toml),
    ("Gemfile", _from_gemfile),
    ("go.mod", _from_go_mod),
]


def detect(path: str) -> list[dict]:
    """Detect frameworks from known config files in a project directory.

    Args:
        path: Root directory to scan.

    Returns:
        List of dicts: [{"framework": "Django", "source": "requirements.txt"}, ...]
    """
    root = Path(path).resolve()
    results: list[dict] = []
    seen: set[str] = set()

    for filename, detector in _DETECTORS:
        config_file = root / filename
        if config_file.exists():
            for label in detector(root):
                if label not in seen:
                    seen.add(label)
                    results.append({"framework": label, "source": filename})

    return results
