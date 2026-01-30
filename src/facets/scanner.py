import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Awaitable, Callable, Iterable

import click
import httpx

from src.services.package import HttpService, PackageService

today = datetime.now()
MIN_ACTIVE_MONTHS = 10
MAX_INACTIVE_MONTHS = 60


@dataclass
class PackageData:
    name: str
    status_code: int
    first_upload_date: datetime
    last_upload_date: datetime

    def __post_init__(self):
        # field validation
        if not all(isinstance(d, datetime) for d in (self.first_upload_date, self.last_upload_date)):
            raise TypeError

    @property
    def category(self) -> str:
        if self.status_code == 404:
            return "INVALID / DELISTED"

        if self.status_code != 200:
            return f"UNHANDLED-{self.status_code}"

        valid_package_category = ""
        if _age_in_months(self.last_upload_date) > MAX_INACTIVE_MONTHS:
            valid_package_category = "OUTDATED"
        elif _age_in_months(self.first_upload_date) < MIN_ACTIVE_MONTHS:
            valid_package_category = "RISKY"
        return valid_package_category


PackageDataList = Iterable[PackageData]
ScannerFn = Callable[..., Awaitable[PackageDataList]]


def _age_in_months(dt: datetime) -> int:
    return (today.year - dt.year) * 12 + (today.month - dt.month)


async def scan_pypi(http: HttpService, packages: list[str]) -> PackageDataList:
    def to_date(date_str: str) -> datetime:
        if not date_str:
            return datetime.now()
        # Invalid isoformat issue in CI, hence using format string
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

    client = PackageService(http, url_pattern="https://pypi.org/pypi/{package}/json")
    details = await client.fetch_all(packages)

    packages_data = []
    for package, response in details:
        if response.status_code == 301:
            raise RuntimeError("Invalid pypi url")

        first_upload_date = last_upload_date = None
        _upload_time_field = "upload_time"

        if response.status_code == 200:
            pkg_data = response.json()
            releases = pkg_data["releases"]
            for _, _data in releases.items():
                if _data:
                    first_upload_date = _data[0][_upload_time_field]
                    break

            last_upload_date = pkg_data["urls"][0][_upload_time_field]

        packages_data.append(
            PackageData(
                package,
                status_code=response.status_code,
                first_upload_date=to_date(first_upload_date),
                last_upload_date=to_date(last_upload_date),
            )
        )
    return packages_data


def get_dependencies() -> Iterable:
    packages = set()
    with open("requirements.txt", "r", encoding="U8") as file:
        packages.update(file.read().splitlines())
    return packages


def get_package_names(pkg: str) -> str:
    return pkg.split("=", 1)[0].rstrip().rstrip(">~")


async def scan_all_packages(scanner: ScannerFn, packages: list[str]) -> int:
    bad_count = 0
    limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)

    async with httpx.AsyncClient(limits=limits, timeout=20.0) as client:
        http = HttpService(client)
        results = await scanner(http, packages)

    for package_data in results:
        if package_data.category:
            bad_count += 1
            click.echo(f"{package_data.name}: {package_data.category}")
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


if __name__ == "__main__":
    asyncio.run(scan_all_packages(scan_pypi, ["panda", "isort", "yuhi", "type"]))
