# pylint: disable=W0613
import datetime as dt
from unittest.mock import AsyncMock, patch

import httpx

from src.cli import cli


def test_sample(runner, test_env):
    response = runner.invoke(cli, ["sample", "files"])
    if response.exit_code == 0:
        assert "project.yaml" in response.output
        assert "created" in response.output

        response = runner.invoke(cli, ["sample", "files"])
        assert response.exit_code == 0
        assert "SKIPPING" in response.output
    else:
        assert "NotImplementedError" in response.output


@patch("httpx.AsyncClient.get", new_callable=AsyncMock)
def test_scan(mock_async_fn, runner, test_env):
    now = dt.datetime.now().isoformat(timespec="seconds")
    old = dt.datetime(2020, 1, 1).isoformat(timespec="seconds")
    mock_data = {"yuhi": (200, now, now), "panda": (200, old, old), "type": (404, now, now), "isort": (200, old, now)}

    def mock_response(url: str):
        pkg = url.rsplit("/", maxsplit=2)[-2]
        status, first_upload, last_upload = mock_data[pkg]
        return httpx.Response(
            status_code=status,
            json={"releases": {"0.0.1": [{"upload_time": first_upload}]}, "urls": [{"upload_time": last_upload}]},
        )

    mock_async_fn.side_effect = mock_response
    response = runner.invoke(cli, ["scan"])
    assert response.exit_code == 0
    assert "3 bad package(s)" in response.output
