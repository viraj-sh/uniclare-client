import sys


def run():
    try:
        from uniclare_client.cli.main import cli
    except ModuleNotFoundError as e:
        if e.name in {"typer", "keyring"}:
            sys.exit(
                "Missing CLI deps. Install: uv tool install 'uniclare-client[cli]'"
            )
        raise
    cli()
