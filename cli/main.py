import typer

from cli.auth import auth_app
from cli.profile import profile_app

cli = typer.Typer(
    name="unicli", help="UniCLI — Uniclare command-line client", no_args_is_help=True
)

cli.add_typer(auth_app, help="Authentication and account management.")
cli.add_typer(profile_app, help="View your profile.")

if __name__ == "__main__":
    cli()
