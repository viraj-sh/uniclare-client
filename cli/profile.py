import asyncio

import keyring
import typer
from rich import box, print
from rich.table import Table

from app.api import app
from app.lifecycle import shutdown, startup

profile_app = typer.Typer()


async def _profile():
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
            profile = await app.profile(session_token)
            if profile.status_code != 200:
                print("[bold red]:cross_mark: Unable to fetch profile.")
                print("Please try again.")
                return
            elif profile.status_code == 200:
                table = Table(
                    title="Profile",
                    title_style="bold",
                    box=box.ROUNDED,
                    show_header=False,
                    title_justify="left",
                    padding=(0, 1),
                )
                table.add_column("Field", style="bold cyan", no_wrap=True)
                table.add_column("Value", style="white")
                fields = [
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
                for label, value in fields:
                    table.add_row(label, value if value is not None else "—")
                print(table)
                return
        else:
            print("Unknown Error cannot validate the session.")
            print(
                "Run [bold cyan]unicli logout[/bold cyan] to clear the session & [bold cyan]unicli login[/bold cyan] to sign in."
            )

    finally:
        await shutdown()


@profile_app.command()
def profile():
    """View your personal and academic details."""
    asyncio.run(_profile())
