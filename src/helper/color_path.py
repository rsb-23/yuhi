from pathlib import Path

import click

COLOR_MAP = {
    "new": "green",
    "+": "green",
    "skip": "bright_green",
    "old": "yellow",
    "del": "red",
    "-": "red",
    "": "reset",
}


def formatter(self, format_spec):
    return click.style(str(self), fg=COLOR_MAP[format_spec.lower()])


Path.__format__ = formatter
