import click

from src.__about__ import __version__
from src.commands import add, create, sample


@click.group()
@click.version_option(__version__)
def cli():
    """Yuhi : A casual project setup tool"""


cli.add_command(add)  # noqa
cli.add_command(create)  # noqa
cli.add_command(sample)  # noqa

if __name__ == "__main__":
    cli()
