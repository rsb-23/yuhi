from pathlib import Path

import click


class ColorPath(Path):
    color_map = {"new": "green", "+": "green", "skip": "bright_green", "old": "yellow", "del": "red", "-": "red"}

    def __init__(self, *args):
        super().__init__(*args)
        self._value = super().__str__()

    def __format__(self, format_spec: str):
        format_spec = format_spec.lower()
        if format_spec in self.color_map:
            return click.style(self._value, fg=self.color_map[format_spec])
        return self._value
