# pylint: disable=W0613
import datetime as dt
from unittest.mock import patch

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


def test_scan(runner, test_env):
    now = dt.datetime.now().isoformat(timespec="seconds")
    old = dt.datetime(2020, 1, 1).isoformat(timespec="seconds")
    mock_data = {"yuhi": (200, now, now), "panda": (200, old, old), "type": (404, now, now), "isort": (200, old, now)}

    class FakeHttpService:
        def __init__(self, client):
            self.client = client
            self.mock_data = mock_data

        async def get(self, url):
            pkg = url.rstrip("/").rsplit("/", maxsplit=2)[-2]
            status, first_upload, last_upload = self.mock_data[pkg]
            return httpx.Response(
                status_code=status,
                json={"releases": {"0.0.1": [{"upload_time": first_upload}]}, "urls": [{"upload_time": last_upload}]},
            )

    with patch("src.facets.scanner.HttpService", FakeHttpService):
        response = runner.invoke(cli, ["scan"])
        assert response.exit_code == 0
        assert "3 bad package(s)" in response.output
