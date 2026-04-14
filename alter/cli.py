"""Alter CLI — automate info gathering on databases, languages, and frameworks."""

import typer
from rich.console import Console

from alter.detectors import databases, frameworks, languages
from alter.output.reporter import Reporter, VALID_FORMATS

app = typer.Typer(
    name="alter",
    help="Scan a project directory and report detected languages, frameworks, and databases.",
    add_completion=False,
)
console = Console()


@app.command()
def scan(
    path: str = typer.Argument(".", help="Path to the project directory to scan."),
    output: str = typer.Option(
        "table",
        "--output",
        "-o",
        help=f"Output format: {', '.join(VALID_FORMATS)}.",
    ),
) -> None:
    """Scan a project and report its languages, frameworks, and databases."""
    if output not in VALID_FORMATS:
        console.print(f"[red]Invalid output format '{output}'. Choose from: {', '.join(VALID_FORMATS)}[/red]")
        raise typer.Exit(code=1)

    results = {
        "languages": languages.detect(path),
        "frameworks": frameworks.detect(path),
        "databases": databases.detect(path),
    }

    Reporter(output_format=output).render(results)


def main() -> None:
    app()


if __name__ == "__main__":
    main()
