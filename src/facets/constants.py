# pylint: disable =invalid-name
from enum import StrEnum


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
    pre_commit = "code-lint.yaml"
    pytest = "code-test.yaml"

    def path(self):
        return f"./.github/workflows/{self.value}"
