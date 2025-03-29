import os

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
    (tmp_dir / "requirements.txt").write_text("yuhi\npanda\n")
    (tmp_dir / "main.py").write_text("check=1")

    original_cwd = os.getcwd()
    os.chdir(tmp_dir)
    try:
        yield tmp_dir
    finally:
        # Change back to the original directory
        os.chdir(original_cwd)


# no tests run here
