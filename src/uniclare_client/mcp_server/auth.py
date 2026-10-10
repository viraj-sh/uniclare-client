import os
import secrets
import time

from fastmcp.server.auth import AccessToken, OAuthProvider
from mcp.server.auth.provider import AuthorizationCode, construct_redirect_uri
from mcp.server.auth.settings import ClientRegistrationOptions
from mcp.shared.auth import OAuthToken
from starlette.responses import HTMLResponse, RedirectResponse

from uniclare_client.core.api import app

FORM = """<form method=post>
<input type=hidden name=txn value="{txn}">
<p>{err}</p>
<input name=mobile placeholder="Mobile number" required>
<input name=password type=password placeholder="Password" required>
<button>Sign in</button></form>"""


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
        return f"{str(self.base_url).rstrip('/')}/login?txn={txn}"

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


async def login_handler(request):
    post = request.method == "POST"
    data = await request.form() if post else request.query_params
    txn = data.get("txn")
    if txn not in provider.pending:
        return HTMLResponse("Link expired. Retry from your client.", 400)
    if not post:
        return HTMLResponse(FORM.format(txn=txn, err=""))

    client, p = provider.pending[txn]
    cap = await app.captcha()
    if cap.captcha is None or cap.session_token is None:
        return HTMLResponse(FORM.format(txn=txn, err="Captcha failed, try again"))

    session_token = cap.session_token
    await app.login(
        str(data["mobile"]), str(data["password"]), cap.captcha, session_token
    )
    check = await app.verify_session_token(session_token)
    if check.status != "success" or check.error_code != 0:
        return HTMLResponse(FORM.format(txn=txn, err="Invalid mobile or password"))

    del provider.pending[txn]
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
    return RedirectResponse(
        construct_redirect_uri(str(p.redirect_uri), code=code, state=p.state), 302
    )
