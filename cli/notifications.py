import asyncio

import keyring
import typer
from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.text import Text

from app.api import app
from app.lifecycle import shutdown, startup

noti_app = typer.Typer()


def render_notifications(notifications):
    if not notifications:
        print("No notifications found.")
        return

    panels = []
    for n in notifications:
        title = n.title or "Untitled"
        date = n.date or "—"
        body = n.body or "—"

        content = Text()
        content.append(f"{date}\n", style="dim")
        content.append(body)

        panels.append(
            Panel(
                content,
                title=f"[bold]{title}[/bold]",
                title_align="left",
                border_style="cyan",
                padding=(0, 1),
            )
        )

    print(Group(*panels))


async def _notifications(limit: int):
    await startup()
    try:
        session_token = keyring.get_password("uniclare_cli", "session_token")
        if session_token is None:
            print("Not logged in.")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")
            return
        verify_session_token = await app.verify_session_token(session_token)
        if (
            verify_session_token.status_code != 200
            or verify_session_token.error_code != 0
        ):
            print("[bold red]:cross_mark: Session expired.")
            keyring.delete_password("uniclare_cli", "session_token")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")
        elif (
            verify_session_token.status_code == 200
            and verify_session_token.error_code == 0
        ):
            notifications_list = await app.notifications(session_token)
            if limit <= 0:
                print("[bold red]✗ --limit must be greater than 0.[/bold red]")
                return
            elif limit > 0 and limit < len(notifications_list):
                render_notifications(notifications_list[:limit])
                return
            else:
                print(
                    f"[bold red]:cross_mark: --limit exceeds available notifications. Only {len(notifications_list)} are available."
                )
                return
        else:
            print("Unknown Error cannot validate the session.")
            print(
                "Run [bold cyan]unicli logout[/bold cyan] to clear the session & [bold cyan]unicli login[/bold cyan] to sign in."
            )
            return

    finally:
        await shutdown()


@noti_app.command()
def notifications(
    limit: int = typer.Option(
        5, "--limit", "-n", help="Number of notifications to show."
    ),
):
    """View your latest notifications."""
    asyncio.run(_notifications(limit))
