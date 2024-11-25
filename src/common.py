from __future__ import annotations

import importlib.resources as resource
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

import click

try:
    import tomllib as toml
except ImportError:
    import toml


def read_toml(filename: str):
    with open(filename, "rb") as f:
        content = toml.load(f)
    return content


@contextmanager
def get_template(filename: str):
    # Access file content
    with resource.open_binary("templates", filename) as file:
        yield file


def create_file(filepath: str, content: str | bytes = b""):
    filepath = Path(filepath)
    if filepath.exists():
        click.echo(f"SKIPPING : {filepath} already exists", color=True)
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
