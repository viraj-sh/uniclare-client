import asyncio

import keyring
import typer
from rich import box, print
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from uniclare_client.core.api import app
from uniclare_client.core.lifecycle import shutdown, startup

results_app = typer.Typer(invoke_without_command=True)

console = Console()


def render_result(result):
    sd = result.student_details
    ri = result.result

    meta = Table(box=box.ROUNDED, show_header=False, padding=(0, 1))
    meta.add_column("K1", style="bold cyan", no_wrap=True)
    meta.add_column("V1")
    meta.add_column("K2", style="bold cyan", no_wrap=True)
    meta.add_column("V2")

    status = ri.result or "—"
    status_styled = (
        f"[bold green]{status}[/bold green]"
        if status.lower() == "pass"
        else f"[bold red]{status}[/bold red]"
        if status != "—"
        else status
    )

    meta.add_row(
        "Semester",
        sd.sem or "—",
        "SGPA",
        ri.sgpa or "—",
    )
    meta.add_row(
        "Exam Date",
        sd.exam_date or "—",
        "Percentage",
        f"{ri.percentage}%" if ri.percentage and ri.percentage != "-" else "—",
    )
    meta.add_row("Status", status_styled, "CGPA", ri.cgpa or "—")

    subjects = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold",
        padding=(0, 1),
    )
    subjects.add_column("#", justify="right", style="cyan", no_wrap=True, width=3)
    subjects.add_column("Subject", width=30, overflow="fold")
    subjects.add_column("ESE", justify="right", no_wrap=True, width=4)
    subjects.add_column("Viva", justify="right", no_wrap=True, width=5)
    subjects.add_column("IA", justify="right", no_wrap=True, width=4)
    subjects.add_column("Total", justify="right", no_wrap=True, width=6)
    subjects.add_column("Grade", justify="center", no_wrap=True, width=6)
    subjects.add_column("Remarks", overflow="fold", min_width=8)

    for s in result.subjects:
        subjects.add_row(
            str(s.id or ""),
            s.sub or "—",
            s.ese_marks or "—",
            s.viva_marks or "—",
            s.ia_marks or "—",
            s.total_marks or "—",
            s.grade or "—",
            s.remarks or "—",
        )

    body = Group(meta, "", subjects)
    console.print(Panel(body, title="[bold]Result #[/bold]", border_style="cyan"))


async def _results_list():
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
            results_list = await app.results_list(session_token)
            table = Table(
                title="Results",
                title_style="bold",
                show_header=True,
                title_justify="left",
                padding=(0, 1),
            )
            table.add_column("#", justify="right", style="cyan", no_wrap=True)
            table.add_column("Semester", overflow="fold")
            table.add_column("Exam Date", no_wrap=True)
            table.add_column("Status", no_wrap=True)
            table.add_column("Result Date", no_wrap=True)
            table.add_column("Exam Code", no_wrap=True)
            for i, r in enumerate(results_list, start=1):
                table.add_row(
                    str(i),
                    r.exam_name or "—",
                    r.exam_date or "—",
                    r.status or "—",
                    r.result_date or "—",
                    r.year or "—",
                )

            print(table)
            return
        else:
            print("Unknown Error cannot validate the session.")
            print(
                "Run [bold cyan]unicli logout[/bold cyan] to clear the session & [bold cyan]unicli login[/bold cyan] to sign in."
            )

    finally:
        await shutdown()


async def _results_details(result_no: int):
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
            reg_keyring = keyring.get_password("uniclare_cli", "reg_no")
            if reg_keyring is not None:
                reg_no_input = reg_keyring
            elif profile.status_code == 200 and profile.reg_no is not None:
                reg_no_input = profile.reg_no
                keyring.set_password("uniclare_cli", "reg_no", reg_no_input)
            else:
                print("Could not fetch your registration number.")
                print(
                    "Enter it manually, or run [bold cyan]unicli profile[/bold cyan] to view it."
                )
                reg_no_input = typer.prompt("Registration number")
                keyring.set_password("uniclare_cli", "reg_no", reg_no_input)
            results_list = await app.results_list(session_token)
            if result_no == -1 or (result_no > 0 and result_no < len(results_list)):
                exam_no = results_list[result_no].year
                if exam_no is not None:
                    pass
                else:
                    print("Could not fetch your exam code.")
                    print(
                        "Enter it manually, or run [bold cyan]unicli results[/bold cyan] to view it."
                    )
                    exam_no = typer.prompt("Registration number")
                result_details = await app.result_details(
                    exam_no, reg_no_input, session_token
                )
                render_result(result_details)
            else:
                print("Invalid result number.")
                print(f"Available results: 1-{len(results_list)}.")
                return
        else:
            print("Unknown Error cannot validate the session.")
            print(
                "Run [bold cyan]unicli logout[/bold cyan] to clear the session & [bold cyan]unicli login[/bold cyan] to sign in."
            )

    finally:
        await shutdown()


@results_app.callback()
def results_callback(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        asyncio.run(_results_list())


@results_app.command("list")
def results_list_cmd():
    """List available examination results."""
    asyncio.run(_results_list())


@results_app.command("show")
def results_details(result_no: int = typer.Argument(-1, help="Result number to show")):
    """Show detailed result information."""
    asyncio.run(_results_details(result_no))
