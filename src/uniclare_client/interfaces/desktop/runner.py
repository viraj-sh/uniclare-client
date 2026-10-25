import asyncio
import threading
from typing import Any, Coroutine


class AsyncRunner:
    """Persistent asyncio loop in a background thread. js_api methods are called
    from pywebview's worker threads; they submit coroutines to this loop."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(
            target=self._loop.run_forever, name="app-loop", daemon=True
        )

    def start(self) -> None:
        self._thread.start()

    def run(self, coro: Coroutine[Any, Any, Any]) -> Any:
        return asyncio.run_coroutine_threadsafe(coro, self._loop).result()

    def stop(self) -> None:
        self._loop.call_soon_threadsafe(self._loop.stop)
        self._thread.join()
        self._loop.close()
