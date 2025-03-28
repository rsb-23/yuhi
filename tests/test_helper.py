import pytest

from src.helper.color_path import COLOR_MAP, Path


def test_colored_path():
    test_path = Path("fol/file.py")
    assert not test_path.exists()
    assert Path.cwd()
    for _format in COLOR_MAP:
        assert f"{test_path:{_format}}"

    with pytest.raises(KeyError):
        assert f"{test_path:ko}"
