import click

DICTIONARY = {"facet": "A sub-component of a project"}


class Glossary(click.Group):
    """Dictionary of terms used in the help"""

    def format_help(self, ctx, formatter):
        super().format_help(ctx, formatter)

        with formatter.section("Glossary"):
            formatter.write_dl([*DICTIONARY.items()])
