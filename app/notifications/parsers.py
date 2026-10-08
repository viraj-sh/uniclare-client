import httpx

from app.notifications.schemas import NotificationResponse


def parse_noti(response: httpx.Response) -> list[NotificationResponse]:
    data = response.json()
    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Signin failed with {response.status_code}"
        )
    return [
        NotificationResponse(
            title=noti.get("ftitle"),
            body=noti.get("fbody"),
            date=noti.get("fpushdate"),
        )
        for noti in data
    ]
