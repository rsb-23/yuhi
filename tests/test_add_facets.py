import pytest

from src.cli import cli


@pytest.mark.parametrize(
    "facet", ["contribution", ".gitignore", "license", "pre-commit", "pylint", "pyproject", "readme", "sourcery"]
)
def test_add_facet_help(runner, facet):
    result = runner.invoke(cli, ["add", facet, "--help"])
    assert result.exit_code == 0
