import os
import secrets
import time
from functools import wraps
from urllib.parse import urlparse

from fastmcp.server.auth import AccessToken, OAuthProvider
from mcp.server.auth.provider import AuthorizationCode, construct_redirect_uri
from mcp.server.auth.settings import ClientRegistrationOptions
from mcp.shared.auth import OAuthToken
from starlette.responses import JSONResponse, Response

from uniclare_client.core.api import app

WEB_UI_URL = os.getenv("WEB_UI_URL", "http://localhost:5173").rstrip("/")
_u = urlparse(WEB_UI_URL)
WEB_UI_ORIGIN = f"{_u.scheme}://{_u.netloc}"


class Code(AuthorizationCode):
    session_token: str


class UniProvider(OAuthProvider):
    def __init__(self, base_url: str):
        super().__init__(
            base_url=base_url,
            client_registration_options=ClientRegistrationOptions(enabled=True),
        )
        self.clients = {}
        self.pending = {}
        self.codes = {}

    async def get_client(self, client_id):
        return self.clients.get(client_id)

    async def register_client(self, client_info):
        self.clients[client_info.client_id] = client_info

    async def authorize(self, client, params):
        txn = secrets.token_urlsafe(16)
        self.pending[txn] = (client, params)
        return f"{WEB_UI_URL}/mcp-connect?txn={txn}"

    async def load_authorization_code(self, client, authorization_code):
        return self.codes.get(authorization_code)

    async def exchange_authorization_code(self, client, authorization_code):
        assert isinstance(authorization_code, Code)
        self.codes.pop(authorization_code.code, None)
        return OAuthToken(
            access_token=authorization_code.session_token, token_type="Bearer"
        )

    async def load_access_token(self, token):
        r = await app.verify_session_token(token)
        if r.status == "success" and r.error_code == 0:
            return AccessToken(token=token, client_id="uniclare", scopes=[])
        return None

    async def verify_token(self, token):
        return await self.load_access_token(token)

    async def load_refresh_token(self, client, refresh_token):
        return None

    async def exchange_refresh_token(self, client, refresh_token, scopes):
        raise NotImplementedError

    async def revoke_token(self, token):
        pass


provider = UniProvider(os.getenv("BASE_URL", "http://localhost:8000"))


def cors(handler):
    @wraps(handler)
    async def wrapper(request):
        if request.method == "OPTIONS":
            resp = Response(status_code=204)
        else:
            resp = await handler(request)
        resp.headers["Access-Control-Allow-Origin"] = WEB_UI_ORIGIN
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        resp.headers["Cache-Control"] = "no-store"
        return resp

    return wrapper


@cors
async def connect_info_handler(request):
    entry = provider.pending.get(request.query_params.get("txn"))
    if not entry:
        return JSONResponse({"error": "expired"}, 404)
    client, p = entry
    return JSONResponse({
        "client_name": client.client_name,
        "redirect_uri": str(p.redirect_uri),
    })


@cors
async def complete_handler(request):
    body = await request.json()
    txn = body.get("txn")
    session_token = body.get("session_token")
    entry = provider.pending.get(txn)
    if not entry or not session_token:
        return JSONResponse({"error": "invalid"}, 400)

    check = await app.verify_session_token(session_token)
    if check.status != "success" or check.error_code != 0:
        return JSONResponse({"error": "invalid_session"}, 401)

    del provider.pending[txn]
    client, p = entry
    code = secrets.token_urlsafe(32)
    provider.codes[code] = Code(
        code=code,
        scopes=[],
        expires_at=time.time() + 60,
        client_id=client.client_id,
        code_challenge=p.code_challenge,
        redirect_uri=p.redirect_uri,
        redirect_uri_provided_explicitly=p.redirect_uri_provided_explicitly,
        session_token=session_token,
    )
    return JSONResponse({
        "redirect": construct_redirect_uri(
            str(p.redirect_uri), code=code, state=p.state
        )
    })
