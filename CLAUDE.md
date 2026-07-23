# CLAUDE.md

This file provides guidance for AI assistants (Claude Code and others) working in this repository.

## Project Overview

**Alter** is an offline-first currency exchange web app by [@garythehuman](https://github.com/garythehuman). It is a static Progressive Web App (PWA) with no build system and no dependencies: plain HTML, CSS, and JavaScript.

**License:** GNU General Public License v3.0 (see `LICENSE`). All contributions must be compatible with GPL v3.

## Architecture

- `index.html` / `styles.css` — app shell: single-page converter UI, light/dark theme via `prefers-color-scheme`
- `app.js` — converter logic; fetches rates from `https://open.er-api.com/v6/latest/USD`, persists them in `localStorage` (key `alter-rates-v1`), refreshes in the background when stale (>1 h) or when the connection returns, and falls back to a bundled rate snapshot if the app has never been online
- `sw.js` — service worker; cache-first for the app shell (bump `CACHE_NAME` when shell files change), API requests bypass the cache
- `manifest.json` / `icon.svg` — PWA installability

## Development Workflow

### Branch Strategy

- `main` — stable, production-ready code
- `claude/<description>` — branches created by AI assistants for automated tasks
- Feature branches should be short-lived and merged via pull request

### Git Conventions

- Write clear, descriptive commit messages in the imperative mood (e.g., "Add user authentication module")
- Reference issues or context in commit bodies where relevant
- Do not force-push to `main`
- Commit signing is enabled on this repository (SSH key signing); do not bypass it

### Pull Requests

- Do not open a pull request unless explicitly asked by the project owner
- PR titles should be concise (under 70 characters)
- Include a summary and a brief test plan in the PR body

## AI Assistant Guidelines

### General Approach

- **Read before editing.** Always read a file before modifying it.
- **Minimal footprint.** Only create or change files directly required by the task.
- **No speculative additions.** Do not add error handling, abstractions, comments, or features beyond what was asked.
- **GPL compliance.** Any code added must be compatible with GPL v3. Avoid copying code from incompatibly licensed sources.

### When the Codebase Grows

Update this file whenever significant structural changes occur:

- A new tech stack or language is adopted
- A build system, test runner, or linter is configured
- Environment variables or secrets are introduced
- A database, API layer, or significant new module is added
- New conventions are established by the project owner

### Commands to Run

There is no build, test, or lint tooling. To run the app locally (service workers require http/https):

```bash
# Start development server
python3 -m http.server 8000
# then open http://localhost:8000
```

Deployment is copying the files to any static host.

## File Structure (current)

```
Alter/
├── LICENSE        # GNU General Public License v3.0
├── README.md      # Project description and usage
├── CLAUDE.md      # This file
├── index.html     # App shell / converter UI
├── styles.css     # Styling (light + dark)
├── app.js         # Rates fetching, storage, conversion logic
├── sw.js          # Service worker (offline cache)
├── manifest.json  # PWA manifest
└── icon.svg       # App icon
```

Update this section as files and directories are added.
