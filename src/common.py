from __future__ import annotations

from contextlib import contextmanager
from copy import deepcopy
from functools import partial
from importlib.resources import files

import click

from src.helper.color_path import Path

FILE_PREFIX = "yuhi-"


@contextmanager
def get_template(filename: str, folder: str = "templates"):
    # Access file content
    try:
        resource = files(folder).joinpath(filename)
        with resource.open("r") as file:
            yield file
    except TypeError as e:
        click.echo("NotImplementedError: Python version < 3.10 does not support this feature.")
        raise NotImplementedError from e


get_sample = partial(get_template, folder="samples")
get_workflow = partial(get_template, folder="templates.workflow")


def create_file(filepath: str, content: str | bytes = b"", use_file_prefix=False):
    filepath = Path(filepath)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath:skip} already exists")
        if not use_file_prefix:
            return
        filepath = Path(FILE_PREFIX + filepath.name)
        click.echo(f"USING : {filepath:new} instead")

    if isinstance(content, str):
        content = content.encode()
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_bytes(content)
    click.echo(f"{filepath:new}:1 : created")


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
