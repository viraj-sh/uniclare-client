import asyncio

import typer
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppError
from uniclare_client.core.notifications import Notification
from uniclare_client.interfaces.cli._session import require_valid_session

noti_app = typer.Typer()


def _render(items: list[Notification]) -> None:
    if not items:
        print("No notifications found.")
        return

    panels = []
    for n in items:
        content = Text()
        if n.date:
            content.append(f"{n.date}\n", style="dim")
        content.append(n.body or "—")
        panels.append(
            Panel(
                content,
                title=f"[bold]{n.title}[/bold]",
                title_align="left",
                border_style="cyan",
                padding=(0, 1),
            )
        )
    print(Group(*panels))


async def _notifications(limit: int) -> None:
    if limit <= 0:
        print("[bold red]✗ --limit must be greater than 0.[/bold red]")
        return

    async with App() as app:
        token = await require_valid_session(app)
        if token is None:
            print("Not logged in, or session expired.")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")
            return

        try:
            items = await app.notifications.list(token)
        except AppError as exc:
            print(
                f"[bold red]✗ Could not fetch notifications:[/bold red] {exc.message}"
            )
            return

        _render(items[:limit])


@noti_app.command()
def notifications(
    limit: int = typer.Option(
        5, "--limit", "-n", help="Number of notifications to show."
    ),
) -> None:
    """View your latest notifications."""
    asyncio.run(_notifications(limit))
