BASE_HEADERS: dict[str, str] = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.6",
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "pragma": "no-cache",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/148.0.0.0 Safari/537.36"
    ),
    "x-requested-with": "XMLHttpRequest",
    "sec-ch-ua": '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
}

INDEX_REFERER = "/index.html"
MAIN_REFERER = "/MainPage.html"


def build_headers(
    *,
    base_url: str,
    session_token: str | None = None,
    referer_path: str = INDEX_REFERER,
    form_post: bool = False,
) -> dict[str, str]:
    headers = {
        **BASE_HEADERS,
        "origin": base_url,
        "referer": f"{base_url}{referer_path}",
    }
    if session_token is not None:
        headers["cookie"] = f"PHPSESSID={session_token}"
    if form_post:
        headers["content-type"] = "application/x-www-form-urlencoded; charset=UTF-8"
    return headers
