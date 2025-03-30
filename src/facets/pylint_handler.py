from collections import defaultdict
from operator import itemgetter

import click

from src.helper.color_path import Path

from .pkg_install import run_in_venv

PYLINT_DEFAULT_DISABLES = {"missing-docstring": "C", "duplicate-code": "R"}
NAME_ARG_MAP = {
    "too-many-lines": "max-module-lines",
    "too-many-arguments": "max-args",
    "too-many-boolean-expressions": "max-bool-expr",
    "too-many-instance-attributes": "max-attributes",
}
PYLINT_REPORT = Path("yuhi-pylint.txt")


def get_lint_errors():
    with open(PYLINT_REPORT, "r", encoding="U8") as f:
        lint_errors = f.readlines()
    yield from lint_errors


def _generate_report() -> (dict, dict):
    fetcher = itemgetter(1, -2, -1)

    unique_messages = {x: defaultdict(int) for x in "FEWCR"}
    max_config = {}
    for line in get_lint_errors():
        if not line:
            continue

        code, outbound, name = fetcher(line.split())
        name = name[1:-1]
        if "too-many" in name:
            max_config[name] = max(int(outbound.split("/")[0][1:]), max_config.get(name, 0))
        elif code[0] in "FEWCR":
            unique_messages[code[0]][name] += 1

    for err_name, code0 in PYLINT_DEFAULT_DISABLES.items():
        unique_messages[code0][err_name] = 0
    return unique_messages, max_config


def get_config_arg(check_name):
    return NAME_ARG_MAP.get(check_name, f"max-{check_name[9:]}")


def _run_pylint(folders=None):
    if not folders:
        folders = ["src", "test", "tests"]
    disables = ",".join(["I", "F0001", *PYLINT_DEFAULT_DISABLES.keys()])
    sources = " ".join(f"./{fol}" for fol in folders if Path(fol).exists())

    click.echo(f"Running pylint on: ./*.py {sources}")
    run_in_venv(f"pylint ./*.py {sources} -sn --enable=all --disable={disables} > {PYLINT_REPORT}", check=False)
    click.echo("Report generated")


def get_pylint_config() -> str:
    def get_config_lines() -> str:
        config_lines = [f"{get_config_arg(name)} = {limit}" for name, limit in max_config.items()]
        return "\n".join(sorted(config_lines)) or ""

    _run_pylint()
    unique_messages, max_config = _generate_report()
    disable_errors = "disable=\n\tI,"
    error_sep = "\n\t"
    for k, v in unique_messages.items():
        if v:
            msgs_with_count = (f"{msg}, #{count or 'keep'}" for msg, count in sorted(v.items()))
            disable_errors += f"\n\t# {k}\n\t{error_sep.join(msgs_with_count)}"
    pylint_config = f"""[MAIN]\njobs=2\nignore-patterns=^(?!^(src|tests?|.+.py)$).+$\n
[FORMAT]\nmax-line-length = 130\n
[DESIGN]\n{get_config_lines()}\n
[MESSAGES CONTROL]\n{disable_errors}
"""
    return pylint_config.strip()
