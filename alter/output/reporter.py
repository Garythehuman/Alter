"""Render scan results to the terminal or as structured output."""

import json

from rich.console import Console
from rich.table import Table
from rich import box

console = Console()

VALID_FORMATS = ("table", "json", "markdown")


class Reporter:
    def __init__(self, output_format: str = "table") -> None:
        if output_format not in VALID_FORMATS:
            raise ValueError(f"output_format must be one of {VALID_FORMATS}")
        self.output_format = output_format

    def render(self, results: dict) -> None:
        """Render scan results in the chosen format.

        Args:
            results: Dict with keys "languages", "frameworks", "databases".
                     Each value is a list of dicts as returned by the detectors.
        """
        if self.output_format == "json":
            self._render_json(results)
        elif self.output_format == "markdown":
            self._render_markdown(results)
        else:
            self._render_table(results)

    # ------------------------------------------------------------------
    # Output formats
    # ------------------------------------------------------------------

    def _render_table(self, results: dict) -> None:
        console.print()
        console.rule("[bold cyan]Alter — Project Scan Results[/bold cyan]")
        console.print()

        # Languages table
        if results.get("languages"):
            table = Table(title="Languages", box=box.ROUNDED, show_lines=False)
            table.add_column("Language", style="green")
            table.add_column("Files", justify="right", style="cyan")
            for row in results["languages"]:
                table.add_row(row["language"], str(row["files"]))
            console.print(table)
            console.print()

        # Frameworks table
        if results.get("frameworks"):
            table = Table(title="Frameworks & Libraries", box=box.ROUNDED, show_lines=False)
            table.add_column("Framework", style="magenta")
            table.add_column("Detected in", style="dim")
            for row in results["frameworks"]:
                table.add_row(row["framework"], row["source"])
            console.print(table)
            console.print()

        # Databases table
        if results.get("databases"):
            table = Table(title="Databases", box=box.ROUNDED, show_lines=False)
            table.add_column("Database", style="yellow")
            table.add_column("Detected in", style="dim")
            for row in results["databases"]:
                table.add_row(row["database"], row["source"])
            console.print(table)
            console.print()

        if not any(results.values()):
            console.print("[dim]No languages, frameworks, or databases detected.[/dim]")

    def _render_json(self, results: dict) -> None:
        print(json.dumps(results, indent=2))

    def _render_markdown(self, results: dict) -> None:
        lines = ["# Alter — Project Scan Results", ""]

        if results.get("languages"):
            lines += ["## Languages", "", "| Language | Files |", "|---|---|"]
            for row in results["languages"]:
                lines.append(f"| {row['language']} | {row['files']} |")
            lines.append("")

        if results.get("frameworks"):
            lines += ["## Frameworks & Libraries", "", "| Framework | Detected in |", "|---|---|"]
            for row in results["frameworks"]:
                lines.append(f"| {row['framework']} | {row['source']} |")
            lines.append("")

        if results.get("databases"):
            lines += ["## Databases", "", "| Database | Detected in |", "|---|---|"]
            for row in results["databases"]:
                lines.append(f"| {row['database']} | {row['source']} |")
            lines.append("")

        print("\n".join(lines))
