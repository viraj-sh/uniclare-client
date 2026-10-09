import typer

from cli.auth import auth_app
from cli.notifications import noti_app
from cli.profile import profile_app
from cli.results import results_app

cli = typer.Typer(
    name="unicli", help="UniCLI — Uniclare command-line client", no_args_is_help=True
)

cli.add_typer(auth_app, help="Authentication and account management.")
cli.add_typer(profile_app, help="View your profile.")
cli.add_typer(results_app, name="results", help="View examination results.")
cli.add_typer(noti_app, help="View your notifications.")

if __name__ == "__main__":
    cli()
