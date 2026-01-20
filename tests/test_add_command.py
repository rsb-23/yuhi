# pylint: disable=w0613
from unittest.mock import patch

import pytest

from src.cli import cli


def assert_with_error(result, msg):
    if result.exit_code == 0:
        assert msg in result.output
    else:
        assert "NotImplementedError" in result.output


@pytest.mark.parametrize("facet", ["contribution", ".gitignore", "readme", "sourcery"])
def test_add_facet(test_env, runner, facet):
    """Test adding various facets."""
    result = runner.invoke(cli, ["add", facet])
    print(result.output)
    assert_with_error(result, "created")


def test_add_license(test_env, runner):
    gh_service = "src.facets.repository"
    with (
        patch("questionary.select") as mock_select,
        patch(f"{gh_service}.get_licenses", return_value={"MIT License": "mit"}),
        patch(f"{gh_service}.get_license_content", return_value="[year][fullname]<program>"),
    ):
        mock_select.return_value.ask.return_value = "MIT License"

        result = runner.invoke(cli, ["add", "license"])
        assert_with_error(result, "created")


def test_add_pre_commit(test_env, runner):
    result = runner.invoke(cli, ["add", "pre-commit"])
    assert_with_error(result, "pre-commit run --all-files")


def test_add_pylint(test_env, runner):
    result = runner.invoke(cli, ["add", "pylint"])
    assert_with_error(result, ".pylintrc:1 : created")
