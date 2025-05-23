"""Facets related to git repositories"""

import click
import httpx

from src.common import create_file, get_template
from src.helper import today
from src.helper.constants import RootFile, Template


@click.command("contribution")
def add_contribution():
    """Adds a CONTRIBUTION file to the repo"""
    click.echo("Adding CONTRIBUTION file..")
    create_file(RootFile.contribution)


# @click.command("gitignore")
@click.command(".gitignore")
def add_gitignore():
    """Adds a .gitignore file to git repo"""
    click.echo("Adding .gitignore file..")
    with get_template(Template.gitignore) as f:
        config = f.read()
    create_file(RootFile.gitignore, config)


@click.command("license")
@click.option("--name", default="mit")
def add_license(name):
    """Adds a license based on github template"""
    click.echo(f"Adding {name} license..")
    resp = httpx.get(f"https://api.github.com/licenses/{name}", timeout=90)
    if resp.status_code == 404:
        click.echo(f"Invalid license name {name}", err=True)
        return
    if resp.status_code != 200:
        click.echo("Unknown error", err=True)
        return

    content: str = resp.json()["body"]
    content = content.replace("[year]", str(today().year))
    create_file(RootFile.license, content)
    click.echo("⚠️ replace [fullname] in license with your git user", color=True)


@click.command("readme")
@click.option("--ext", default="md")
def add_readme(ext):
    """Adds a README file to the repo"""
    click.echo(f"Adding readme with {ext}..")
    filename = RootFile.readme
    if ext != "md":
        filename = f"{filename[:-2]}{ext}"
    content = b"# Project Name\n---\nDescription"
    create_file(filename, content)
