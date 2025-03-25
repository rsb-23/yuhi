import click

from src.common import append_file, create_file, get_template, get_workflow, read_toml
from src.helper.constants import RootFile, Template, Workflow

from .pylint_handler import get_pylint_config


@click.command("pre-commit")
def add_pre_commit():
    """Integrates pre-commit tool"""
    click.echo("setting up pre-commit..")
    with get_template(RootFile.pre_commit_yaml) as f:
        config = f.read()
    create_file(RootFile.pre_commit_yaml, config)

    with get_template(Template.pre_commit_pref) as f:
        config = f.read()
        black, flake8, isort = config.split(b"\r\n\r\n")
    config_map = {"black": black, "flake8": flake8, "isort": isort}
    current_config = read_toml(RootFile.pyproject_toml)
    config = ""
    for tool in ("black", "flake8", "isort"):
        if tool not in current_config["tool"]:
            config += f"\n\n{config_map[tool].decode()}"
        else:
            click.echo(f"\tSKIPPED : {tool} is already configured")
    if config:
        append_file(RootFile.pyproject_toml, config)

    click.echo("adding pre-commit workflow...")
    with get_workflow(Workflow.pre_commit) as f:
        config = f.read()
    create_file(Workflow.pre_commit.path(), config)

    # TODO: run installations and autoupdates, after .venv setup
    click.echo("-- pre-commit files created. --\nNow run below commands:", color=True)
    click.echo("\tpre-commit install && pre-commit autoupdate")
    click.echo("\tpre-commit run --all-files")


@click.command("pylint")
def add_pylint():
    """Adds pylint facet"""
    click.echo("adding pylint...")
    create_file(RootFile.pylint, get_pylint_config(), use_file_prefix=True)

    with get_template(Template.pylint) as f:
        config = f.read()
    append_file(RootFile.pre_commit_yaml, config)


@click.command("sourcery")
def add_sourcery():
    """Adds sourcery facet"""
    click.echo("adding sourcery...")
    with get_template(RootFile.sourcery_config) as f:
        config = f.read()
    create_file(RootFile.sourcery_config, config)
