import asyncio

import keyring
import typer
from keyring.errors import PasswordDeleteError
from rich import print

from uniclare_client.core.api import App
from uniclare_client.core.errors import AppError, InvalidCredentials, InvalidInput

auth_app = typer.Typer()

KEYRING_SERVICE = "uniclare_cli"  # keep old name so existing saved sessions survive
KEYRING_KEY = "session_token"


def _get_token() -> str | None:
    return keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)


def _save_token(token: str) -> None:
    keyring.set_password(KEYRING_SERVICE, KEYRING_KEY, token)


def _clear_token() -> None:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_KEY)
    except PasswordDeleteError:
        pass


async def _login(mobile: str | None) -> None:
    async with App() as app:
        token = _get_token()
        if token is not None:
            if await app.auth.verify_session(token):
                print("[bold green]✓ An active session already exists.[/bold green]")
                print(
                    "Use [bold cyan]unicli logout[/bold cyan] "
                    "before logging in with another account."
                )
                return
            _clear_token()
            print("Existing session is expired or invalid.")

        print("Fetching captcha...")
        try:
            captcha = await app.auth.get_captcha()
        except AppError as exc:
            print(f"[bold red]✗ Captcha failed:[/bold red] {exc.message}")
            return

        print(f"Captcha: [bold]{captcha.value}[/bold]")
        captcha_input = typer.prompt("Enter Captcha", type=int)

        if mobile is None:
            mobile = typer.prompt("Mobile number")
        else:
            print(f"Using mobile number: {mobile}")

        password = typer.prompt("Password", hide_input=True)

        print("Logging in...")
        try:
            session = await app.auth.login(
                reg_no=mobile,
                password=password,
                captcha_code=captcha_input,
                session_token=captcha.session_token,
            )
        except InvalidCredentials as exc:
            print(f"[bold red]✗ Login failed:[/bold red] {exc.message}")
            return

        _save_token(session.token)
        print("[bold green]✓ Login successful.[/bold green]")
        print("[bold green]✓ Session saved securely.[/bold green]")


async def _logout() -> None:
    async with App() as app:
        token = _get_token()
        if token is None:
            print("You are not logged in.")
            return

        if await app.auth.verify_session(token):
            try:
                await app.auth.logout(token)
            except AppError as exc:
                print(f"[bold red]✗ Logout failed:[/bold red] {exc.message}")
                print("Your local session was not removed.")
                return
            _clear_token()
            print("[bold green]✓ Logged out successfully.[/bold green]")
            print("Your local session was removed.")
        else:
            _clear_token()
            print("Existing session was already expired.")
            print("Your local session was removed.")


async def _status() -> None:
    async with App() as app:
        token = _get_token()
        if token is None:
            print("Not logged in.")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")
            return

        if await app.auth.verify_session(token):
            print("[bold green]✓ Logged in.[/bold green]")
            print("Session: Valid")
        else:
            _clear_token()
            print("[bold red]✗ Session expired.[/bold red]")
            print("Run [bold cyan]unicli login[/bold cyan] to sign in.")


async def _reset_password(mobile: str | None) -> None:
    async with App() as app:
        print("Fetching captcha...")
        try:
            captcha = await app.auth.get_captcha()
        except AppError as exc:
            print(f"[bold red]✗ Captcha failed:[/bold red] {exc.message}")
            return

        if mobile is None:
            mobile = typer.prompt("Mobile number")
        else:
            print(f"Using mobile number: {mobile}")

        print("Sending OTP...")
        try:
            info = await app.auth.request_otp(mobile_no=mobile)
        except InvalidInput as exc:
            print(f"[bold red]✗ Failed to send OTP:[/bold red] {exc.message}")
            return

        if info.message:
            print(info.message)

        otp_code = typer.prompt("OTP")
        new_password = typer.prompt("New Password", hide_input=True)
        confirm = typer.prompt("Confirm Password", hide_input=True)
        while new_password != confirm:
            print("[bold red]✗ Passwords do not match.[/bold red]")
            new_password = typer.prompt("New Password", hide_input=True)
            confirm = typer.prompt("Confirm Password", hide_input=True)

        try:
            await app.auth.reset_password(
                mobile_no=mobile,
                otp_code=otp_code,
                new_password=new_password,
                session_token=captcha.session_token,
            )
        except AppError as exc:
            print(f"[bold red]✗ Password reset failed:[/bold red] {exc.message}")
            return

        print("[bold green]✓ Password reset successfully.[/bold green]")
        print(
            "Log in using [bold cyan]unicli login[/bold cyan] with your new password."
        )


@auth_app.command()
def login(
    mobile: str | None = typer.Option(
        None, "--mobile", help="Registered mobile number"
    ),
) -> None:
    """Sign in to your Uniclare account."""
    asyncio.run(_login(mobile))


@auth_app.command()
def logout() -> None:
    """Sign out of your current session."""
    asyncio.run(_logout())


@auth_app.command()
def status() -> None:
    """Check the current session."""
    asyncio.run(_status())


@auth_app.command()
def reset_password(
    mobile: str | None = typer.Option(
        None, "--mobile", help="Registered mobile number"
    ),
) -> None:
    """Reset your account password."""
    asyncio.run(_reset_password(mobile))
