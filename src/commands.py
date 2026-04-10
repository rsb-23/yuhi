import click

from src.facets import SUBGROUP_ADD, SUBGROUP_CREATE
from src.facets.scanner import run_scan
from src.helper.file_handler import create_file, get_sample


@click.group()
def add():
    """Adds a facet to the project"""


for cmd in SUBGROUP_ADD:
    add.add_command(cmd)


@click.group()
def create():
    """Creates complete project structure"""


for cmd in SUBGROUP_CREATE:
    create.add_command(cmd)


@click.command()
@click.argument("name", type=click.Choice(["files", "project"]))
def sample(name):
    """Adds a sample yaml file to local"""
    if name == "files":
        sample_name = "project.yaml"
    else:
        sample_name = f"{name}.yaml"
    create_file(sample_name, content=get_sample(sample_name))


@click.command()
def scan():
    """lists all bad packages in requirements.txt"""
    run_scan()
