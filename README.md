# Alter

Alter scans a project directory and reports its programming languages, frameworks, and databases — automatically.

## Usage

```bash
# Scan the current directory
alter scan .

# Scan a specific project
alter scan /path/to/project

# Output as JSON
alter scan . --output json

# Output as Markdown
alter scan . --output markdown
```

## Installation

```bash
pip install -e ".[dev]"
```

Requires Python 3.11+.

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
