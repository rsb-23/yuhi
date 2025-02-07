from itertools import count

import click
from requests import Session

s = Session()


def scan_pypi(package, index):
    response = s.get(f"https://pypi.org/pypi/{package}/json")
    if response.status_code == 404:
        click.echo(f"{next(index):>2} {package}")


def get_dependencies() -> iter:
    packages = set()
    with open("requirements.txt", "r", encoding="U8") as file:
        packages.update(file.read().splitlines())
    return packages


def get_package_names(pkg: str) -> str:
    return pkg.split("=", 1)[0].rstrip().rstrip(">~")


def run_scan(package_repo: str = "pypi"):
    package_repo = package_repo.lower()
    if package_repo == "pypi":
        _scanner = scan_pypi
    else:
        click.echo("Unsupported package repository")
        return

    packages = [get_package_names(x) for x in get_dependencies()]
    click.echo(f"Scanning {len(packages)} packages ...")

    index = count(1)
    for package in packages:
        _scanner(package, index)

    click.echo(f"{next(index) - 1} bad package(s) found")
    s.close()
