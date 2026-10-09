import typer

from cli.auth import auth_app

cli = typer.Typer(
    name="unicli", help="UniCLI — Uniclare command-line client", no_args_is_help=True
)

cli.add_typer(auth_app, help="Authentication Commands")


if __name__ == "__main__":
    cli()
