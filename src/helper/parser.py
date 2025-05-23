from ruamel.yaml import YAML

try:
    import tomllib as toml
except ImportError:
    import toml  # noqa

yaml = YAML(typ="rt")
yaml.indent(mapping=2, sequence=4, offset=2)
yaml.preserve_quotes = True
yaml.width = 100
yaml.line_break = True


def read_toml(filename: str) -> dict:
    try:
        with open(filename, "rb") as f:
            content = toml.load(f)
    except TypeError:
        with open(filename, "r", encoding="U8") as f:
            content = toml.load(f)
    return content


def read_yaml(filename: str) -> dict:
    with open(filename, "rb") as f:
        content = yaml.load(f)
    return content
