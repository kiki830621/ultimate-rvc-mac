"""
Module which defines the command-line interface for the Ultimate RVC
project.
"""

from __future__ import annotations

import typer

from ultimate_rvc.cli.generate.main import app as generate_app
from ultimate_rvc.cli.train.main import app as train_app

app = typer.Typer(
    name="urvc-cli",
    no_args_is_help=True,
    help="CLI for the Ultimate RVC project",
    rich_markup_mode="markdown",
)

app.add_typer(generate_app)
app.add_typer(train_app)


if __name__ == "__main__":
    app()
