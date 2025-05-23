# pylint: disable =invalid-name
from enum import Enum

try:
    from enum import StrEnum
except ImportError:

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


class Template(StrEnum):
    gitignore = "gitignore.txt"
    pre_commit_pref = "pre_commit.toml"
    tests = "tests.toml"


class Workflow(StrEnum):
    pre_commit = "code-lint.yml"
    pytest = "code-test.yml"

    def path(self):
        return f"./.github/workflows/{self.value}"
