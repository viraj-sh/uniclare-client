import asyncio

import typer
from rich import box, print
from rich.table import Table

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppError
from uniclare_client.core.profile import Profile
from uniclare_client.interfaces.cli._session import require_valid_session

profile_app = typer.Typer()


def _render(profile: Profile) -> None:
    table = Table(
        title="Profile",
        title_style="bold",
        title_justify="left",
        box=box.ROUNDED,
        show_header=False,
        padding=(0, 1),
    )
    table.add_column("Field", style="bold cyan", no_wrap=True)
    table.add_column("Value", style="white")

    rows = [
        ("Name", profile.full_name),
        ("Father's Name", profile.fat_name),
        ("Mother's Name", profile.mot_name),
        ("Degree", profile.degree),
        ("College", profile.college),
        ("Registration No.", profile.reg_no),
        ("Mobile", profile.mob_no),
        ("Email", profile.email),
        ("Category", profile.category),
        ("Fee Type", profile.fee_type),
    ]
    for label, value in rows:
        table.add_row(label, value if value else "—")

    print(table)


async def _profile() -> None:
    async with App() as app:
        token = await require_valid_session(app)
        if token is None:
            print("Not logged in, or session expired.")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")
            return

        try:
            profile = await app.profile.get(token)
        except AppError as exc:
            print(f"[bold red]✗ Could not fetch profile:[/bold red] {exc.message}")
            return

        _render(profile)


@profile_app.command()
def profile() -> None:
    """View your personal and academic details."""
    asyncio.run(_profile())
