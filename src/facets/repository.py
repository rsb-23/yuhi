"""Facets related to git repositories"""

import re

import click
import questionary

from src.common import create_file, get_template
from src.helper import Path, today
from src.helper.constants import RootFile, Template
from src.services import get_git_user, get_license_content, get_licenses


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
def add_license():
    """Adds a license based on github template"""

    filepath = Path(RootFile.license)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath:skip} already exists")
        return

    licenses = get_licenses()
    license_choices = list(licenses.keys())

    name = questionary.select("Select a license", choices=license_choices).ask()
    click.echo(f"Adding {name} license..")

    year, author = str(today().year), get_git_user() or "<AUTHOR>"
    content: str = get_license_content(key=licenses[name])
    tags = re.findall(r"[\[<][\w\s]+[>\]]", content)
    print(tags)
    for tag in tags:
        if tag[1:5] in ("year", "yyyy"):
            new_val = year
        elif "name" in tag:
            new_val = author
        else:
            new_val = tag
        content = content.replace(tag, new_val)

    if create_file(RootFile.license, content):
        click.echo(f"LICENSE ADDED: {name}", color=True)


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
