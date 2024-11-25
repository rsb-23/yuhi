import click

from src.facets import SUBGROUP_ADD, SUBGROUP_CREATE


@click.group()
def add():
    """Adds a facet to the project"""


for cmds in SUBGROUP_ADD:
    add.add_command(cmds)


@click.group()
def create():
    """Creates complete project structure"""


for cmds in SUBGROUP_CREATE:
    create.add_command(cmds)
