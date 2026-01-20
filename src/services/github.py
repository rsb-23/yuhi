# pragma: no cover
from functools import lru_cache

import httpx


@lru_cache(1)
def get_licenses() -> dict:
    """Fetches all available licenses from Github"""
    response = httpx.get("https://api.github.com/licenses", timeout=5.0)
    response.raise_for_status()
    return {x["name"]: x["key"] for x in response.json()}


@lru_cache(3)
def get_license_content(key) -> str | None:
    resp = httpx.get(f"https://api.github.com/licenses/{key}", timeout=90)
    resp.raise_for_status()
    return resp.json()["body"]
