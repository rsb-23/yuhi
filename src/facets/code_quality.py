import click

from src.common import append_file, create_file, get_template, get_workflow
from src.helper import color_echo, read_toml, read_yaml, yaml
from src.helper.color_path import Path
from src.helper.constants import RootFile, Template, Workflow

from .pylint_handler import get_pylint_config


def _add_hooks_yaml(*hooks: str):
    def add_space_to_bracket(x):
        return x.replace("[", "[ ").replace("]", " ]")

    # Get current and template configs
    pre_commit_yaml = Path(RootFile.pre_commit_yaml)
    if not pre_commit_yaml.exists():
        pre_commit_yaml.write_text("repos: []\n", encoding="U8")
    current_config = read_yaml(RootFile.pre_commit_yaml)

    with get_template(RootFile.pre_commit_yaml) as f:
        template_config = yaml.load(f)
    hooks = hooks or template_config["default_hooks"]

    # check hook id before merge
    _current_hooks = set()
    for repo in current_config["repos"]:
        if repo.get("repo", "").endswith("pre-commit/pre-commit-hooks"):
            _current_hooks.add("pre-commit-hooks")
            continue
        if "hooks" not in repo:
            continue
        for hook in repo["hooks"]:
            _current_hooks.add(hook["id"])
    for hook in hooks:
        if hook in _current_hooks:
            continue
        current_config["repos"].append(template_config[hook])
        click.echo(f"\tADDED : {hook}")

    print("writing to pre-commit-yaml file")
    with open(RootFile.pre_commit_yaml, "w", encoding="U8") as f:
        yaml.dump(current_config, f, transform=add_space_to_bracket)


def _add_hooks_toml(*hooks: str):
    """Adds [tool.hook] configs in toml file"""
    with get_template(Template.pre_commit_pref) as f:
        config = f.read()
        black, flake8, isort = config.split("\n\n")
    config_map = {"black": black, "flake8": flake8, "isort": isort}

    pyproject = Path(RootFile.pyproject_toml)
    if not pyproject.exists():
        pyproject.write_text("", encoding="U8")

    current_config = read_toml(RootFile.pyproject_toml)

    config = ""
    for hook in hooks:
        if hook not in current_config.get("tool", {}):
            config += f"\n\n{config_map[hook]}"
        else:
            click.echo(f"\tSKIPPED : {hook} is already configured")
    if config:
        append_file(RootFile.pyproject_toml, config)


@click.command("pre-commit")
def add_pre_commit():
    """Integrates pre-commit tool"""
    click.echo("setting up pre-commit..")
    _add_hooks_yaml()
    _add_hooks_toml("black", "flake8", "isort")

    click.echo("adding pre-commit workflow...")
    with get_workflow(Workflow.pre_commit) as f:
        config = f.read()
    create_file(Workflow.pre_commit.path(), config)

    # TODO: run installations and autoupdates, after .venv setup
    click.echo("-- pre-commit files created. --\nNow run below commands:")
    color_echo("\tpre-commit install && pre-commit autoupdate", "cyan")
    color_echo("\tpre-commit run --all-files", "cyan")


@click.command("pylint")
def add_pylint():
    """Adds pylint facet"""
    click.echo("adding pylint...")
    create_file(RootFile.pylint, get_pylint_config(), use_file_prefix=True)

    _add_hooks_yaml("pylint")


@click.command("sourcery")
def add_sourcery():
    """Adds sourcery facet"""
    click.echo("adding sourcery...")
    with get_template(RootFile.sourcery_config) as f:
        config = f.read()
    create_file(RootFile.sourcery_config, config)
