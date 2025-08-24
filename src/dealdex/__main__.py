"""Command line interface for Deal-Dex."""

from pathlib import Path

import typer

app = typer.Typer(help="Deal-Dex command line interface.")


@app.command()
def scan(rules: Path = typer.Argument(...)) -> None:
    """Scan marketplaces using the provided RULES file."""
    typer.echo(f"Scanning for deals using {rules}")


if __name__ == "__main__":
    app()
