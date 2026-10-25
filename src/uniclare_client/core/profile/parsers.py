import httpx

from uniclare_client.core.clients.http import read_json
from uniclare_client.core.errors import InvalidResponse
from uniclare_client.core.profile.schema import Profile


def _error_code(data: dict) -> int:
    raw = data.get("error_code", 0)
    if raw is None:
        return 0
    try:
        return int(raw)
    except (TypeError, ValueError):
        raise InvalidResponse(f"non-integer error_code: {raw!r}")


def parse_profile(response: httpx.Response) -> Profile:
    if response.status_code != 200:
        try:
            msg = response.json().get("msg") or f"HTTP {response.status_code}"
        except ValueError:
            msg = f"HTTP {response.status_code}"
        raise InvalidResponse(f"profile: {msg}")

    data = read_json(response)
    if _error_code(data) != 0:
        raise InvalidResponse(f"profile: {data.get('msg') or 'vendor error'}")

    return Profile(
        reg_no=data["strRegno"],
        full_name=data["fname"],
        degree=data["fdegree"],
        fat_name=data.get("ffatname"),
        mot_name=data.get("fmotname"),
        degree_code=data.get("fdeggrp"),
        college=data.get("college"),
        college_code=data.get("fcollcode"),
        photo=data.get("photo"),
        category=data.get("category"),
        fee_type=data.get("feetype"),
        mob_no=data.get("strMobile"),
        email=data.get("strEmail"),
        parent_mob_no=data.get("strParentMob"),
    )
