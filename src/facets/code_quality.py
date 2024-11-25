import click

from src.common import append_file, create_file, get_template

from .constants import RootFile, Template


@click.command("pre-commit")
def add_pre_commit():
    """Integrates pre-commit tool"""
    click.echo("setting up pre-commit..")
    with get_template(RootFile.pre_commit_yaml) as f:
        config = f.read()
    create_file(RootFile.pre_commit_yaml, config)

    with get_template(Template.pre_commit_pref) as f:
        config = f.read()
    append_file(RootFile.pyproject_toml, config)

    # TODO: run installations and autoupdates, after .venv setup


@click.command("sourcery")
def add_sourcery():
    """Adds sourcery facet"""
    click.echo("adding sourcery...")
    with get_template(RootFile.sourcery_config) as f:
        config = f.read()
    create_file(RootFile.sourcery_config, config)
