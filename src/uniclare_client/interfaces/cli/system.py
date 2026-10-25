import asyncio

import typer
from rich import print

from uniclare_client.core.api import App

system_app = typer.Typer()


async def _health() -> None:
    async with App() as app:
        status = await app.health()

    all_ok = all(status.values())
    if all_ok:
        print("[bold green]✓[/bold green] Healthy")
    else:
        print("[bold red]✗[/bold red] Unhealthy")

    for name, ok in status.items():
        mark = "[green]✓[/green]" if ok else "[red]✗[/red]"
        print(f"{mark} {name}")


@system_app.command()
def health() -> None:
    """Check the application's health."""
    asyncio.run(_health())
