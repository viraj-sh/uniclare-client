import keyring
from keyring.errors import PasswordDeleteError

from uniclare_client.core.api import App

KEYRING_SERVICE = "uniclare_cli"
KEYRING_KEY = "session_token"


def get_token() -> str | None:
    return keyring.get_password(KEYRING_SERVICE, KEYRING_KEY)


def save_token(token: str) -> None:
    keyring.set_password(KEYRING_SERVICE, KEYRING_KEY, token)


def clear_token() -> None:
    try:
        keyring.delete_password(KEYRING_SERVICE, KEYRING_KEY)
    except PasswordDeleteError:
        pass


async def require_valid_session(app: App) -> str | None:
    """Return the stored token if it verifies; clear and return None otherwise."""
    token = get_token()
    if token is None:
        return None
    if not await app.auth.verify_session(token):
        clear_token()
        return None
    return token
