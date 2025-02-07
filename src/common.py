from __future__ import annotations

import importlib.resources as resource
from contextlib import contextmanager
from datetime import datetime
from functools import partial
from pathlib import Path

import click

try:
    import tomllib as toml
except ImportError:
    import toml

FILE_PREFIX = "yuhi-"


def read_toml(filename: str):
    with open(filename, "rb") as f:
        content = toml.load(f)
    return content


@contextmanager
def get_template(filename: str, folder="templates"):
    # Access file content
    with resource.open_binary(folder, filename) as file:
        yield file


get_sample = partial(get_template, folder="samples")


def create_file(filepath: str, content: str | bytes = b"", use_file_prefix=False):
    filepath = Path(filepath)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath} already exists", color=True)
        if use_file_prefix:
            filepath = Path(FILE_PREFIX + filepath.name)
            click.echo(f"USING : {filepath} instead", color=True)
        else:
            return
    if isinstance(content, str):
        content = content.encode()
    with open(filepath, "wb") as fw:
        fw.write(content)
    click.echo(f"CREATED : {filepath}")


def append_file(filepath: str, content: str | bytes):
    if isinstance(content, str):
        content = content.encode()
    with open(filepath, "ab") as fw:
        fw.write(content)
    click.echo(f"UPDATED : {filepath}")


def today() -> datetime:
    return datetime.now()
