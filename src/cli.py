import click

from src.__about__ import __version__
from src.commands import add, create, sample, scan
from src.glossary import Glossary


@click.group(cls=Glossary)
@click.version_option(__version__, "-V", "--version")
@click.help_option("-h", "--help")
def cli():
    """Yuhi : A casual project setup tool"""


cli.add_command(add)  # noqa
cli.add_command(create)  # noqa
cli.add_command(sample)  # noqa
cli.add_command(scan)  # noqa

if __name__ == "__main__":
    cli()
