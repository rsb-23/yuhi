"""first tests"""

import pytest

from src.cli import cli


def test_yuhi_help(runner):
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize("command", ["add", "create", "sample", "scan"])
def test_command_help(runner, command):
    result = runner.invoke(cli, [command, "--help"])
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "facet", ["contribution", ".gitignore", "license", "pre-commit", "pylint", "pyproject", "readme", "sourcery"]
)
def test_add_facet_help(runner, facet):
    result = runner.invoke(cli, ["add", facet, "--help"])
    assert result.exit_code == 0
