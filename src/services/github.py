# pragma: no cover
import httpx

GITHUB_API = "https://api.github.com"


def get_licenses() -> dict:
    """Fetches all available licenses from Github"""
    response = httpx.get(f"{GITHUB_API}/licenses", timeout=5.0)
    response.raise_for_status()
    return {x["name"]: x["key"] for x in response.json()}


def get_license_content(key) -> str | None:
    resp = httpx.get(f"{GITHUB_API}/licenses/{key}", timeout=90)
    resp.raise_for_status()
    return resp.json()["body"]
