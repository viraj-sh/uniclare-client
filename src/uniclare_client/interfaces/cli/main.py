import typer

from uniclare_client.interfaces.cli.auth import auth_app
from uniclare_client.interfaces.cli.profile import profile_app
from uniclare_client.interfaces.cli.results import results_app
from uniclare_client.interfaces.cli.system import system_app

cli = typer.Typer(
    name="unicli", help="UniCLI — Uniclare command-line client", no_args_is_help=True
)

cli.add_typer(system_app)
cli.add_typer(auth_app)
cli.add_typer(results_app, name="results", help="View examination results.")
cli.add_typer(profile_app)

if __name__ == "__main__":
    cli()
