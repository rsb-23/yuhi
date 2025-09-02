import os
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="session")
def runner():
    return CliRunner()


@pytest.fixture(scope="session")
def test_env(tmp_path_factory):
    """
    Creates a complete test environment with predefined structure

    path = %temp%/pytest-of-App
    """
    tmp_dir = tmp_path_factory.getbasetemp()
    (tmp_dir / "is_tmp").touch()  # mandatory for debugging

    # Add sample data
    sample_req = "\n".join(["yuhi", "panda", "type", "isort"])
    (tmp_dir / "requirements.txt").write_text(sample_req)
    (tmp_dir / "main.py").write_text(get_test_code())

    original_cwd = os.getcwd()
    os.chdir(tmp_dir)
    try:
        yield tmp_dir
    finally:
        # Change back to the original directory
        os.chdir(original_cwd)


def get_test_code() -> str:
    with open("tests/test_files/code.txt", "r", encoding="U8") as f:
        return f.read()


@pytest.fixture
def mock_httpx_get():
    with patch("httpx.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        yield mock_get


# no tests run here
