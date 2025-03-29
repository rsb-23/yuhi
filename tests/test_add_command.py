# pylint: disable=w0613
import pytest

from src.cli import cli


@pytest.mark.parametrize("facet", ["contribution", ".gitignore", "license", "readme", "sourcery"])
def test_add_facet(test_env, runner, facet):
    result = runner.invoke(cli, ["add", facet])
    assert result.exit_code == 0
    assert "created" in result.output


def test_add_pre_commit(test_env, runner):
    result = runner.invoke(cli, ["add", "pre-commit"])
    assert result.exit_code == 0
    assert "pre-commit run --all-files" in result.output


def test_add_pylint(test_env, runner):
    (test_env / ".pre-commit-config.yaml").write_text("")
    result = runner.invoke(cli, ["add", "pylint"])
    assert result.exit_code == 0
    assert ".pylintrc:1 : created" in result.output
