from __future__ import annotations

import importlib.resources as resource
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
from functools import partial

import click

from src.helper.color_path import ColorPath

try:
    import tomllib as toml
except ImportError:
    import toml

FILE_PREFIX = "yuhi-"


def read_toml(filename: str) -> dict:
    with open(filename, "rb") as f:
        content = toml.load(f)
    return content


@contextmanager
def get_template(filename: str, folder="templates"):
    # Access file content
    with resource.open_binary(folder, filename) as file:
        yield file


get_sample = partial(get_template, folder="samples")
get_workflow = partial(get_template, folder="templates.workflow")


def create_file(filepath: str, content: str | bytes = b"", use_file_prefix=False):
    filepath = ColorPath(filepath)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath:skip} already exists")
        if not use_file_prefix:
            return
        filepath = ColorPath(FILE_PREFIX + filepath.name)
        click.echo(f"USING : {filepath:new} instead")

    if isinstance(content, str):
        content = content.encode()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "wb") as fw:
        fw.write(content)
    click.echo(f"{filepath:new}:1 : created")


def append_file(filepath: str, content: str | bytes):
    filepath = ColorPath(filepath)
    if isinstance(content, str):
        content = content.encode()
    with open(filepath, "r", encoding="U8") as fw:
        count = len(fw.readlines())
    with open(filepath, "ab") as fw:
        fw.write(content)
    click.echo(f"{filepath:old}:{count + 1} : content appended")


def today() -> datetime:
    return datetime.now()


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
