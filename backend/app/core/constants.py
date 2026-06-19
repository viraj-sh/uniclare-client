from typing import Optional


BASE_HEADERS: dict = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.6",
    "cache-control": "no-cache",
    "connection": "keep-alive",
    "origin": "https://studentportal.universitysolutions.in",
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


def unauthenticated_headers(referer: Optional[str] = None) -> dict:
    if referer is not None:
        referer_url = referer
    else:
        referer_url = "https://studentportal.universitysolutions.in/index.html"
    return {
        **BASE_HEADERS,
        "referer": referer_url,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    }


def authenticated_headers(session_token: str, referer: Optional[str] = None) -> dict:
    if referer is not None:
        referer_url = referer
    else:
        referer_url = "https://studentportal.universitysolutions.in/MainPage.html"
    return {
        **BASE_HEADERS,
        "referer": referer_url,
        "cookie": f"PHPSESSID={session_token}",
    }
