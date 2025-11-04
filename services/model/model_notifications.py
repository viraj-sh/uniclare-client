from dataclasses import dataclass
from typing import Optional, Any, Dict, List


@dataclass
class Notification:

    title: str
    body: str
    date: str

    @classmethod
    def from_json(cls, data: Dict[str, Any]) -> Optional["Notification"]:

        if not isinstance(data, dict):
            return None

        title = data.get("ftitle")
        body = data.get("fbody")
        date = data.get("fpushdate")

        if not title or not body or not date:
            return None

        return cls(title=title, body=body, date=date)
