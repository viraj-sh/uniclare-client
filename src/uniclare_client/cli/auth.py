import asyncio

import keyring
import typer
from rich import print

from uniclare_client.core.api import app
from uniclare_client.core.lifecycle import shutdown, startup

auth_app = typer.Typer()


async def _login(mobile_no: str | None = None):
    await startup()
    try:
        session_token = keyring.get_password("uniclare_cli", "session_token")
        if session_token is not None:
            verify_session_token = await app.verify_session_token(session_token)
            if (
                verify_session_token.status_code == 200
                and verify_session_token.error_code == 0
            ):
                print(
                    "[bold green]:heavy_check_mark: An active session already exists."
                )
                print(
                    "Use [bold cyan]unicli logout[/bold cyan] before logging in with another account"
                )
                return
            else:
                keyring.delete_password("uniclare_cli", "session_token")
                print("Existing session is expired or invalid")
        print("Fetching captcha...")
        captcha = await app.captcha()
        if captcha.captcha is None or captcha.session_token is None:
            print("Failed to generate captcha")
            print("Try [bold cyan]unicli login[/bold cyan] again")
            return
        print(f"Captcha: {captcha.captcha}")
        captcha_input = typer.prompt("Enter Captcha")
        if mobile_no is None:
            mobile = typer.prompt("Mobile number")
        else:
            mobile = mobile_no
            print(f"Using Mobile number: {mobile_no}")
        password = typer.prompt("Password", hide_input=True)
        print("Logging in...")
        login = await app.login(mobile, password, captcha_input, captcha.session_token)
        if login.status_code == 200 and login.error_code == "0":
            print("[bold green]:heavy_check_mark: Login successful.")
            keyring.set_password("uniclare_cli", "session_token", captcha.session_token)
            print("[bold green]:heavy_check_mark: Session saved securely.")
            return
        else:
            print("[bold red]:cross_mark: Login Failed")
            if login.message:
                print(f"{login.message}")
            else:
                print("An unexpected error occurred.")
            return

    finally:
        await shutdown()


async def _logout():
    await startup()
    try:
        session_token = keyring.get_password("uniclare_cli", "session_token")
        if session_token is None:
            print("You are not logged in.")
            return
        if session_token is not None:
            verify_session_token = await app.verify_session_token(session_token)
            if (
                verify_session_token.status_code == 200
                and verify_session_token.error_code == 0
            ):
                logout = await app.logout(session_token)
                if logout.status_code == 200 and logout.message == "logout":
                    print("[bold green]:heavy_check_mark: Logged out successfully.")
                    keyring.delete_password("uniclare_cli", "session_token")
                    print("Your local session was removed.")
                    return
                else:
                    print("[bold red]:cross_mark: Unable to log out from Uniclare.")
                    print("Your local session was not removed.")
            else:
                print("Existing session is expired or invalid")
                keyring.delete_password("uniclare_cli", "session_token")
                print("Your local session was removed.")
                return
    finally:
        await shutdown()


async def _status():
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
            print("[bold green]:heavy_check_mark: Logged in.")
            print("Session: Valid")
        else:
            print("Unknown Error cannot validate the session.")
            print(
                "Run [bold cyan]unicli logout[/bold cyan] to clear the session & [bold cyan]unicli login[/bold cyan] to sign in."
            )

    finally:
        await shutdown()


async def _reset_password(mobile_no: str | None = None):
    await startup()
    try:
        captcha = await app.captcha()
        if captcha.captcha is None or captcha.session_token is None:
            print("Failed to generate captcha")
            print("Try [bold cyan]unicli reset-password[/bold cyan] again")
            return
        if mobile_no is None:
            mobile = typer.prompt("Mobile number")
        else:
            mobile = mobile_no
            print(f"Using Mobile number: {mobile_no}")
        print("Sending OTP...")
        otp = await app.otp(mobile, captcha.session_token)
        if otp.status_code != 200 or otp.email is None or otp.status == "error":
            print("[bold red]:cross_mark: Failed to send OTP.")
            if otp.message is not None:
                print(otp.message)
            else:
                print("Please try again.")
            return
        elif (
            otp.status_code == 200 and otp.email is not None and otp.status == "success"
        ):
            print(otp.message)
        else:
            print("[bold yellow]![/] OTP request returned an unexpected response.")
            print("Please try again.")
            return
        otp_input = typer.prompt("OTP")
        new_password = typer.prompt("New Password", hide_input=True)
        confirm_password = typer.prompt("Confirm Password", hide_input=True)
        while new_password != confirm_password:
            print("[bold red]:cross_mark: Password do not match")
            new_password = typer.prompt("New Password", hide_input=True)
            confirm_password = typer.prompt("Confirm Password", hide_input=True)
        reset_password = await app.reset_password(
            mobile, otp_input, new_password, captcha.session_token
        )
        if reset_password.status_code != 200 or reset_password.status != "success":
            print("[bold red]:cross_mark: Password reset failed.")
            print("Please check your OTP and mobile number, then try again.")
            return
        elif reset_password.status_code == 200 and reset_password.status == "success":
            print("[bold green]:heavy_check_mark: Password reset successfully.")
            print(
                "Log in using [bold cyan]unicli login[/bold cyan] with your new password"
            )
        else:
            print("[bold red]:cross_mark: Could not reset password.")
            print("Unexpected server response. Please try again later.")
            return
    finally:
        await shutdown()


@auth_app.command()
def login(
    mobile: str | None = typer.Option(
        None, "--mobile", help="Registered mobile number"
    ),
):
    """Sign in to your Uniclare account."""
    asyncio.run(_login(mobile))


@auth_app.command()
def logout():
    """Sign out of your current session."""
    asyncio.run(_logout())


@auth_app.command()
def status():
    """Check the current session."""
    asyncio.run(_status())


@auth_app.command()
def reset_password(
    mobile: str | None = typer.Option(
        None, "--mobile", help="Registered mobile number"
    ),
):
    """Reset your account password."""
    asyncio.run(_reset_password(mobile))
