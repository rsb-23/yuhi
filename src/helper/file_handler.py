from copy import deepcopy
from importlib.resources import files
from typing import Protocol

import click
from ruamel.yaml import YAML

from .color_path import Path

try:
    import tomllib as toml
except ImportError:
    # py3.10
    import toml  # noqa

yaml = YAML(typ="rt")
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.width = 100
yaml.line_break = True

FILE_PREFIX = "yuhi-"


class HasPath(Protocol):
    # pylint: disable =r0903
    def from_path(self) -> Path:
        pass


def copy_to_local(*, source, destination):
    """Copies files from pkg resource to local project without change"""
    config = read_text(source)
    create_file(destination, config)


def read_text(filename: Path | HasPath) -> str:
    if hasattr(filename, "from_path"):
        filename = filename.from_path()
    with filename.open("r") as f:
        content = f.read()
    return content


def read_toml(filename: Path | HasPath) -> dict:
    if hasattr(filename, "from_path"):
        filename = filename.from_path()
    try:
        with filename.open("rb") as f:
            content = toml.load(f)
    except TypeError:
        with filename.open("r", encoding="U8") as f:
            content = toml.load(f)
    return content


def read_yaml(filename: Path | HasPath) -> dict:
    if hasattr(filename, "from_path"):
        filename = filename.from_path()
    with filename.open("rb") as f:
        content = yaml.load(f)
    return content


def get_sample(filename: str) -> str:
    resource = files("samples").joinpath(filename)
    with resource.open() as file:
        return file.read()


# File Write
def create_file(filepath: str, content: str | bytes = b"", use_file_prefix=False) -> bool:
    filepath = Path(filepath)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath:skip} already exists")
        if not use_file_prefix:
            return False
        filepath = Path(FILE_PREFIX + filepath.name)
        click.echo(f"USING : {filepath:new} instead")

    if isinstance(content, str):
        content = content.encode()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(content)
    click.echo(f"{filepath:new}:1 : created")
    return True


def append_file(filepath: str, content: str | bytes):
    filepath = Path(filepath)
    if isinstance(content, str):
        content = content.encode()
    with open(filepath, "r", encoding="U8") as fw:
        count = len(fw.readlines())
    with open(filepath, "ab") as fw:
        fw.write(content)
    click.echo(f"{filepath:old}:{count + 1} : content appended")


def deep_merge(dict1: dict, dict2: dict) -> dict:
    result = deepcopy(dict1)

    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = deep_merge(result[key], value)
        else:
            # Override or add values from dict2
            result[key] = deepcopy(value)

    return result
