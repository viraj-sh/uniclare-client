from importlib.resources import as_file, files
from pathlib import Path

import webview
from platformdirs import user_data_dir

from uniclare_client.core.api import App
from uniclare_client.interfaces.desktop.bridge import JsApi
from uniclare_client.interfaces.desktop.runner import AsyncRunner


def run() -> None:
    runner = AsyncRunner()
    runner.start()
    app = App()
    runner.run(app.start())
    api = JsApi(runner, app)

    storage_path = Path(user_data_dir("uniclare_client", appauthor=False)) / "webview"
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
            )
    finally:
        runner.run(app.close())
        runner.stop()
