import httpx

from uniclare_client.core.clients.http import read_json
from uniclare_client.core.errors import InvalidResponse
from uniclare_client.core.notifications.schema import Notification


def parse_notifications(response: httpx.Response) -> list[Notification]:
    if response.status_code != 200:
        raise InvalidResponse(f"notifications: HTTP {response.status_code}")

    data = read_json(response)

    # Vendor quirk: success returns a JSON array, errors return a dict
    # with error_code/msg. Handle both.
    if isinstance(data, dict):
        raw = data.get("error_code", 0)
        try:
            code = int(raw) if raw is not None else 0
        except (TypeError, ValueError):
            raise InvalidResponse(f"notifications: non-integer error_code: {raw!r}")
        if code != 0:
            raise InvalidResponse(f"notifications: {data.get('msg') or 'vendor error'}")
        raise InvalidResponse("notifications: unexpected dict response")

    if not isinstance(data, list):
        raise InvalidResponse("notifications: response is not a list")

    return [
        Notification(
            title=item["ftitle"],
            body=item.get("fbody"),
            date=item.get("fpushdate"),
        )
        for item in data
        if isinstance(item, dict) and item.get("ftitle")
    ]
