import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import click
import httpx

today = datetime.now()
MIN_PACKAGE_YEAR = today.year - 5
MAX_PACKAGE_YEAR = today.year - 1


@dataclass
class PackageData:
    name: str
    status_code: int
    first_upload_date: datetime
    last_upload_date: datetime


async def scan_pypi(client: httpx.AsyncClient, package: str) -> PackageData:
    def to_date(date_str: str) -> datetime:
        if not date_str:
            return datetime.now()
        return datetime.fromisoformat(date_str)

    response = await client.get(f"https://pypi.org/pypi/{package}/json")

    first_upload_date = last_upload_date = None
    _upload_time_field = "upload_time_iso_8601"

    if response.status_code == 200:
        pkg_data = response.json()
        releases = pkg_data["releases"]
        first_release = releases[list(releases.keys())[0]]

        first_upload_date = first_release[0][_upload_time_field]
        last_upload_date = pkg_data["urls"][0][_upload_time_field]

    return PackageData(package, response.status_code, to_date(first_upload_date), to_date(last_upload_date))


def get_dependencies() -> iter:
    packages = set()
    with open("requirements.txt", "r", encoding="U8") as file:
        packages.update(file.read().splitlines())
    return packages


def get_package_names(pkg: str) -> str:
    return pkg.split("=", 1)[0].rstrip().rstrip(">~")


async def scan_all_packages(scanner: Callable, packages: list[str]) -> int:
    bad_count = 0
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)

    async with httpx.AsyncClient(limits=limits, timeout=20.0) as client:
        tasks = [scanner(client, package) for package in packages]
        results: list[PackageData] = await asyncio.gather(*tasks, return_exceptions=True)

    for package_data in results:
        if package_data.status_code == 404:
            bad_count += 1
            click.echo(f"{package_data.name}: INVALID")
        elif package_data.status_code == 200:
            if package_data.last_upload_date.year < MIN_PACKAGE_YEAR:
                bad_count += 1
                click.echo(f"{package_data.name}: OUTDATED")
            elif package_data.first_upload_date.year > MAX_PACKAGE_YEAR:
                bad_count += 1
                click.echo(f"{package_data.name}: RISKY")
    return bad_count


def run_scan(package_repo: str = "pypi"):
    package_repo = package_repo.lower()
    if package_repo == "pypi":
        _scanner = scan_pypi
    else:
        click.echo("Unsupported package repository")
        return

    packages = [get_package_names(x) for x in get_dependencies()]
    click.echo(f"Scanning {len(packages)} packages ...")
    bad_pkg_count = asyncio.run(scan_all_packages(_scanner, packages))

    click.echo(f"{bad_pkg_count} bad package(s) found")
