import asyncio

import typer
from rich import box, print
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppError
from uniclare_client.core.results import Result, ResultSummary
from uniclare_client.interfaces.cli._session import require_valid_session

results_app = typer.Typer(invoke_without_command=True)
console = Console()


def _render_detail(result: Result) -> None:
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
    percentage = f"{ri.percentage}%" if ri.percentage and ri.percentage != "-" else "—"

    meta.add_row("Semester", sd.sem or "—", "SGPA", ri.sgpa or "—")
    meta.add_row("Exam Date", sd.exam_date or "—", "Percentage", percentage)
    meta.add_row("Status", status_styled, "CGPA", ri.cgpa or "—")

    subjects = Table(
        box=box.ROUNDED, show_header=True, header_style="bold", padding=(0, 1)
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

    title = sd.sem or "Result Details"
    console.print(
        Panel(
            Group(meta, "", subjects),
            title=f"[bold]{title}[/bold]",
            border_style="cyan",
        )
    )


def _render_list(summaries: list[ResultSummary]) -> None:
    table = Table(
        title="Results",
        title_style="bold",
        title_justify="left",
        show_header=True,
        padding=(0, 1),
    )
    table.add_column("#", justify="right", style="cyan", no_wrap=True)
    table.add_column("Semester", overflow="fold")
    table.add_column("Exam Date", no_wrap=True)
    table.add_column("Status", no_wrap=True)
    table.add_column("Result Date", no_wrap=True)
    table.add_column("Exam Code", no_wrap=True)

    for i, r in enumerate(summaries, start=1):
        table.add_row(
            str(i),
            r.exam_name or "—",
            r.exam_date or "—",
            r.status or "—",
            r.result_date or "—",
            r.year or "—",
        )

    print(table)
    print(
        "\nUse [bold cyan]results show <#[/bold cyan] to view details "
        "(e.g. [bold cyan]results show 1[/bold cyan])."
    )


async def _results_list() -> None:
    async with App() as app:
        token = await require_valid_session(app)
        if token is None:
            print("Not logged in, or session expired.")
            print("Run [bold cyan]uniclare-client login[/bold cyan] to sign in.")
            return

        try:
            summaries = await app.results.list(token)
        except AppError as exc:
            print(f"[bold red]✗ Could not fetch results:[/bold red] {exc.message}")
            return

        if not summaries:
            print("No results available.")
            return

        _render_list(summaries)


async def _results_details(result_no: int) -> None:
    async with App() as app:
        token = await require_valid_session(app)
        if token is None:
            print("Not logged in, or session expired.")
            print("Run [bold cyan]uniclare-client login[/bold cyan] to sign in.")
            return

        try:
            summaries = await app.results.list(token)
        except AppError as exc:
            print(f"[bold red]✗ Could not fetch results:[/bold red] {exc.message}")
            return

        if not summaries:
            print("No results available.")
            return

        if result_no == -1:
            summary = summaries[-1]
        elif 1 <= result_no <= len(summaries):
            summary = summaries[result_no - 1]
        else:
            print(
                f"[bold red]✗ Invalid result number.[/bold red] Available: 1-{len(summaries)}."
            )
            return

        try:
            detail = await app.results.details(
                exam_no=summary.year,
                reg_no=summary.reg_no,
                session_token=token,
            )
        except AppError as exc:
            print(f"[bold red]✗ Could not fetch result:[/bold red] {exc.message}")
            return

        _render_detail(detail)


@results_app.callback()
def results_callback(ctx: typer.Context) -> None:
    if ctx.invoked_subcommand is None:
        asyncio.run(_results_list())


@results_app.command("list")
def results_list_cmd() -> None:
    """List available examination results."""
    asyncio.run(_results_list())


@results_app.command("show")
def results_details(
    result_no: int = typer.Argument(-1, help="Result number to show (default: latest)"),
) -> None:
    """Show detailed result information."""
    asyncio.run(_results_details(result_no))
