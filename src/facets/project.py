from __future__ import annotations

import click

from src.helper import yaml
from src.helper.color_path import Path


@click.command("pyproject")
def add_pyproject():
    """Adds pyproject.toml file"""
    click.echo("NOT IMPLEMENTEDŪ")
    # pyproject = read_toml(RootFile.pyproject_toml)
    # print(pyproject["tool"]["black"])


def _create_files(structure_data: str | list | dict, parent_path=Path()):
    """Recursively traverses a nested YAML structure and create files"""
    if isinstance(structure_data, dict):
        for key, value in structure_data.items():
            _create_files(value, parent_path / key)
    elif isinstance(structure_data, list):
        for item in structure_data:
            _create_files(item, parent_path)
    else:
        # Makes parent folders and blank file
        file = parent_path / structure_data
        parent_path.mkdir(parents=True, exist_ok=True)
        try:
            file.touch(exist_ok=False)
            click.echo(f"CREATED : {file!s}")
        except FileExistsError:
            click.echo(f"SKIPPED : {file!s}")


@click.command("files")
@click.option("--structure-file", "-s", default="project.yaml", required=True)
def create_structure(structure_file: str):
    """Creates all folders and files as structured in project.yaml"""
    filename = Path(structure_file)
    assert filename.suffix in {".yml", ".yaml"}, "Only YAML file is supported"
    with open(filename, "rb") as f:
        data = yaml.load(f)

    try:
        project_name = data["project"]["name"]
    except KeyError:
        click.echo("project.name is missing", err=True, color=True)
        return
    if project_name not in data:
        click.echo(f"No project structure available for '{project_name}'", err=True)
        return

    _create_files(structure_data=data[project_name], parent_path=Path(project_name))
