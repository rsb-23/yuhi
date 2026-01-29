# pylint: disable =invalid-name
from importlib.resources import files
from pathlib import Path

try:
    from enum import Enum, StrEnum
except ImportError:
    # py3.10
    from enum import Enum

    class StrEnum(str, Enum):
        def __str__(self):
            return str(self.value)


class Facet(StrEnum):
    contribution = "contribution"
    git = "git"
    gitignore = ".gitignore"
    license = "license"
    pre_commit = "pre-commit"
    pyproject = "pyproject"
    readme = "readme"
    sourcery = "sourcery"


class RootFile(StrEnum):
    contribution = "CONTRIBUTING.md"
    gitignore = ".gitignore"
    license = "LICENSE"
    pre_commit_yaml = ".pre-commit-config.yaml"
    pylint = ".pylintrc"
    pyproject_toml = "pyproject.toml"
    readme = "README.md"
    sourcery_config = ".sourcery.yaml"

    def from_path(self):
        return Path(self.value)

    def template(self):
        return files("templates").joinpath(self.value)


class Template(StrEnum):
    gitignore = "gitignore.txt"
    pre_commit_pref = "pre_commit.toml"
    tests = "tests.toml"

    def from_path(self):
        return files("templates").joinpath(self.value)


class Workflow(StrEnum):
    pre_commit = "code-lint.yml"
    pytest = "code-test.yml"

    def from_path(self):
        return files("templates.workflow").joinpath(self.value)

    def to_path(self):
        return Path("./.github/workflows") / self.value
