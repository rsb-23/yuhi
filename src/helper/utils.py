from datetime import datetime

import click


def color_echo(text, color, **kwargs):
    if color or kwargs:
        text = click.style(text, fg=color, **kwargs)
    click.echo(text)


def today() -> datetime:
    return datetime.now()
