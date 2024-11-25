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


class RootFile:
    contribution = "CONTRIBUTING.md"
    gitignore = ".gitignore"
    license = "LICENSE"
    pre_commit_yaml = ".pre-commit-config.yaml"
    pyproject_toml = "pyproject.toml"
    readme = "README.md"
    sourcery_config = ".sourcery.yaml"


class Template:
    gitignore = "gitignore.txt"
    pre_commit_pref = "pre_commit.toml"
    tests = "tests.toml"
