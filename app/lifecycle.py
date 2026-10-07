from app.clients.http import close_http_client, init_http_client


async def startup():
    await init_http_client()


async def shutdown():
    await close_http_client()
