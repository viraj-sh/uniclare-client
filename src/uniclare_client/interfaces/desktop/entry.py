import socket
import sys
import time
from importlib.resources import as_file, files
from pathlib import Path

import webview
from platformdirs import user_data_dir

from uniclare_client.core.api import App
from uniclare_client.interfaces.desktop.bridge import JsApi
from uniclare_client.interfaces.desktop.runner import AsyncRunner


def _wait_for_port(port: int, timeout: float = 3.0) -> bool:
    """Return True if port is free (or becomes free within timeout)."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return True
            except OSError:
                time.sleep(0.2)
    return False


def run() -> None:
    runner = AsyncRunner()
    runner.start()
    app = App()
    runner.run(app.start())
    api = JsApi(runner, app)

    port = app.config.desktop_http_port
    if not _wait_for_port(port):
        runner.run(app.close())
        runner.stop()
        sys.exit(
            f"Port {port} is already in use.\n"
            f"An instance of Uniclare may already be running, or another\n"
            f"application is using this port.\n"
            f"\n"
            f"- Close any running Uniclare window, then try again.\n"
            f"- If no window is visible, a previous process may be stuck —\n"
            f"  find and terminate it, then try again.\n"
            f"- To use a different port (note: this resets your saved session):\n"
            f"    UNICLARE_DESKTOP_HTTP_PORT={port + 1} unidesk"
        )

    storage_path = Path(user_data_dir("uniclare-client", appauthor=False)) / "webview"
    storage_path.mkdir(parents=True, exist_ok=True)

    try:
        with as_file(
            files("uniclare_client.interfaces.desktop") / "static"
        ) as static_dir:
            webview.create_window(
                "Uniclare",
                str(static_dir / "index.html"),
                js_api=api,
            )
            webview.start(
                private_mode=False,
                storage_path=str(storage_path),
                http_server=True,
                http_port=port,
            )
    finally:
        runner.run(app.close())
        runner.stop()
