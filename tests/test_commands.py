import pytest

from src.cli import cli


@pytest.mark.parametrize("command", ["add", "create", "sample", "scan"])
def test_command_help(runner, command):
    result = runner.invoke(cli, [command, "--help"])
    assert result.exit_code == 0


# def test_create_structure_help(runner):
#     result = runner.invoke(cli, ["create", "structure", "--help"])
#     assert result.exit_code == 0
