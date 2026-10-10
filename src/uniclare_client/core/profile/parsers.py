import httpx

from uniclare_client.core.profile.schemas import ProfileResult


def parse_profile(response: httpx.Response) -> ProfileResult:
    data = response.json()
    if response.status_code != 200:
        raise ValueError(
            f"{data.get('error_code')} -> {data.get('msg')}"
            or f"Fetching User Profile with {response.status_code}"
        )
    return ProfileResult(
        status_code=response.status_code,
        full_name=data.get("fname"),
        fat_name=data.get("ffatname"),
        mot_name=data.get("fmotname"),
        degree=data.get("fdegree"),
        degree_code=data.get("fdeggrp"),
        college=data.get("college"),
        college_code=data.get("fcollcode"),
        photo=data.get("photo"),
        category=data.get("category"),
        fee_type=data.get("feetype"),
        reg_no=data.get("strRegno"),
        mob_no=data.get("strMobile"),
        email=data.get("strEmail"),
        parent_mob_no=data.get("strParentMob"),
    )
