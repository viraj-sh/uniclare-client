import socket
import threading
import time

import uvicorn
import webview
from app.core.config import settings
from app.main import app

HOST = settings.webview_host
port = settings.webview_port


def run_server(port: int) -> None:
    uvicorn.run(
        app,
        host=HOST,
        port=port,
        reload=False,
        log_level="info",
    )


def wait_until_ready(port: int) -> None:
    while True:
        try:
            with socket.create_connection((HOST, port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)


server = threading.Thread(target=run_server, args=(port,), daemon=True)
server.start()
wait_until_ready(port)

window = webview.create_window(
    title="Uniclare Client",
    url=f"http://{HOST}:{port}",
    js_api=None,
    width=1200,
    height=800,
)
webview.start(private_mode=False, debug=False, gui="qt")
