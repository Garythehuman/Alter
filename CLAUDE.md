# CLAUDE.md

This file provides guidance for AI assistants (Claude Code and others) working in this repository.

## Project Overview

**Alter** is a project by [@garythehuman](https://github.com/garythehuman), currently in its earliest stage. As of the last update to this file, the repository contains only a license and a minimal README — no source code, build system, or dependencies yet.

**License:** GNU General Public License v3.0 (see `LICENSE`). All contributions must be compatible with GPL v3.

## Repository State

The project is greenfield. When source code, configuration, or tooling is added, this file should be updated to reflect:

- The project's purpose and tech stack
- Directory structure and key files
- Build, test, and lint commands
- Environment setup instructions
- Code conventions and style rules

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

### Commands to Run (update when applicable)

Once a build system is in place, document the essential commands here. For example:

```bash
# Install dependencies
<command>

# Run tests
<command>

# Lint / format
<command>

# Build for production
<command>

# Start development server
<command>
```

Replace the placeholders above with actual commands once the project is initialized.

## File Structure (current)

```
Alter/
├── LICENSE        # GNU General Public License v3.0
├── README.md      # Project title only — to be expanded
└── CLAUDE.md      # This file
```

Update this section as files and directories are added.
