import sys

import typer

from uniclare_client.core.errors import AppError


def _exit_code(err: AppError) -> int:
    if err.code in {"invalid_credentials", "session_expired", "authentication_error"}:
        return 2
    if err.code in {
        "external_timeout",
        "external_unavailable",
        "rate_limited",
        "invalid_response",
    }:
        return 3
    if err.code in {"invalid_input", "not_found"}:
        return 4
    if err.code == "config_error":
        return 5
    return 1


def run() -> None:
    try:
        from uniclare_client.interfaces.cli.main import cli
    except ModuleNotFoundError as exc:
        if exc.name in {"typer", "keyring"}:
            sys.exit(
                "Missing CLI deps. Install: uv tool install 'uniclare-client[cli]'"
            )
        raise

    try:
        cli()
    except AppError as exc:
        typer.echo(f"{exc.code}: {exc.message}", err=True)
        sys.exit(_exit_code(exc))
