# pylint: disable=w0613

import pytest

from src.cli import cli


def assert_with_error(result, msg):
    if result.exit_code == 0:
        assert msg in result.output
    else:
        assert "NotImplementedError" in result.output


@pytest.mark.parametrize("facet", ["contribution", ".gitignore", "license", "readme", "sourcery"])
def test_add_facet(test_env, runner, facet):
    """Test adding various facets."""
    result = runner.invoke(cli, ["add", facet])
    print(result.output)
    assert_with_error(result, "created")


def test_add_pre_commit(test_env, runner):
    result = runner.invoke(cli, ["add", "pre-commit"])
    assert_with_error(result, "pre-commit run --all-files")


def test_add_pylint(test_env, runner):
    result = runner.invoke(cli, ["add", "pylint"])
    assert_with_error(result, ".pylintrc:1 : created")
