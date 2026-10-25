from contextlib import AsyncExitStack
from dataclasses import dataclass

from uniclare_client.core.clients.http import HttpClient
from uniclare_client.core.config import Settings


@dataclass
class Resources:
    http: HttpClient


async def start(config: Settings, stack: AsyncExitStack) -> Resources:
    http = HttpClient(config)
    await http.start()
    stack.push_async_callback(http.close)
    return Resources(http=http)
