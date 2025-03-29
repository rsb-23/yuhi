from pathlib import Path

import click

COLOR_MAP = {"new": "green", "+": "green", "skip": "bright_green", "old": "yellow", "del": "red", "-": "red"}


def formatter(self, format_spec):
    _path = str(self)
    return click.style(_path, fg=COLOR_MAP[format_spec.lower()]) if format_spec else _path


Path.__format__ = formatter
