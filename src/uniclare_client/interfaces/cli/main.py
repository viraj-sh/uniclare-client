import typer

from uniclare_client.interfaces.cli.system import system_app

cli = typer.Typer(
    name="unicli", help="UniCLI — Uniclare command-line client", no_args_is_help=True
)

cli.add_typer(system_app, help="")

if __name__ == "__main__":
    cli()
