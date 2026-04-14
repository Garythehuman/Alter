# CLAUDE.md

This file provides guidance for AI assistants (Claude Code and others) working in this repository.

## Project Overview

**Alter** is a CLI tool that automates information gathering about a project's tech stack — detecting programming languages, frameworks, and databases by scanning directories and config files.

**License:** GNU General Public License v3.0. All contributions must be GPL v3 compatible.

**Entry point:** `alter scan [path]` — scans a directory and outputs a report.

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11+ |
| CLI framework | Typer |
| Terminal output | Rich |
| HTTP client | httpx |
| Config parsing | PyYAML, tomllib (stdlib 3.11+) |
| Testing | pytest |
| Packaging | pyproject.toml + setuptools |

## Directory Structure

```
Alter/
├── alter/                   # Main package
│   ├── __init__.py          # Version string
│   ├── cli.py               # Typer app and entry point
│   ├── detectors/           # Detection modules
│   │   ├── languages.py     # Detects languages by file extension
│   │   ├── frameworks.py    # Detects frameworks from config files
│   │   └── databases.py     # Detects databases from env/config/deps
│   └── output/
│       └── reporter.py      # Renders results (table, json, markdown)
├── tests/
│   ├── test_languages.py
│   ├── test_frameworks.py
│   └── test_databases.py
├── pyproject.toml           # Project config, dependencies, scripts
├── CLAUDE.md                # This file
├── README.md
└── LICENSE                  # GNU GPL v3
```

## Development Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install package with dev dependencies
pip install -e ".[dev]"

# Run the CLI
alter scan .
alter scan /path/to/project --output json
alter scan /path/to/project --output markdown
```

## Commands

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=alter

# Run a specific test file
pytest tests/test_languages.py

# Install in editable mode (re-run after changing pyproject.toml)
pip install -e ".[dev]"
```

## Architecture

### Detection Flow

1. User runs `alter scan <path>`
2. `cli.py` calls each detector: `languages.detect()`, `frameworks.detect()`, `databases.detect()`
3. Each detector returns a list of dicts (see formats below)
4. `Reporter.render()` formats and prints the combined results

### Detector Return Formats

```python
# languages.detect(path) -> list[dict]
[{"language": "Python", "files": 12}, ...]

# frameworks.detect(path) -> list[dict]
[{"framework": "Django", "source": "requirements.txt"}, ...]

# databases.detect(path) -> list[dict]
[{"database": "PostgreSQL", "source": ".env"}, ...]
```

### Adding a New Detector

- Add new file under `alter/detectors/`
- Export it from `alter/detectors/__init__.py`
- Add the `detect(path: str) -> list[dict]` function
- Wire it into `alter/cli.py`
- Add tests under `tests/`

### Adding a New Framework/Database

- For JS frameworks: extend `JS_FRAMEWORK_MAP` in `detectors/frameworks.py`
- For Python packages: extend `PYTHON_FRAMEWORK_MAP` in `detectors/frameworks.py`
- For databases: extend `DEPENDENCY_PATTERNS` or `URL_SCHEME_MAP` in `detectors/databases.py`

### Adding a New Output Format

- Add the format name to `VALID_FORMATS` in `alter/output/reporter.py`
- Add a `_render_<format>()` method to `Reporter`
- Add a branch in `Reporter.render()`

## Code Conventions

- **Type hints everywhere** — all function signatures must be fully typed
- **Docstrings on public functions** — Args and Returns sections, plain English
- **No global state** — detectors are stateless functions; Reporter is a small class
- **Fail silently on bad files** — detectors catch exceptions and return empty results rather than crashing
- **One responsibility per file** — each detector handles one detection domain only

## Git Conventions

- `main` — stable branch; do not push directly
- `claude/<description>` — AI-generated feature branches
- Commit messages: imperative mood, concise (e.g. `Add Ruby framework detection`)
- Do not force-push to `main`
- Commit signing is enabled (SSH); do not bypass with `--no-verify`

## AI Assistant Guidelines

- **Read before editing** — always read a file before modifying it
- **Minimal footprint** — only create or change what the task requires
- **No speculative additions** — do not add extra error handling, abstractions, or features beyond what was asked
- **GPL compliance** — do not copy code from incompatibly licensed sources
- **Update this file** when significant structural changes are made (new modules, new commands, new dependencies)
