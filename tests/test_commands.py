# pylint: disable=W0613

from src.cli import cli


def test_sample(runner, test_env):
    response = runner.invoke(cli, ["sample", "files"])
    assert response.exit_code == 0
    assert "project.yaml" in response.output
    assert "created" in response.output

    response = runner.invoke(cli, ["sample", "files"])
    assert response.exit_code == 0
    assert "SKIPPING" in response.output


def test_scan(runner, test_env):
    response = runner.invoke(cli, ["scan"])
    assert response.exit_code == 0
    assert "1 bad package(s)" in response.output
