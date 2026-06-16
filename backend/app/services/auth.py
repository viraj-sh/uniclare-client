from app.core.http import HTTPClientDep
from app.core.urls import AuthUrls


async def signin(mob_no: str, password: str, client: HTTPClientDep):
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.6",
        "cache-control": "no-cache",
        "connection": "keep-alive",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://studentportal.universitysolutions.in",
        "pragma": "no-cache",
        "referer": "https://studentportal.universitysolutions.in/index.html",
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
    payload = {"regno": mob_no, "passwd": password}
    return await client.post(url=AuthUrls.SIGNIN, headers=headers, json=payload)
