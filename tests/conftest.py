from contextlib import chdir

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

    with chdir(tmp_dir):
        yield tmp_dir


def get_test_code() -> str:
    with open("tests/test_files/code.txt", encoding="U8") as f:
        return f.read()


# no tests run here
