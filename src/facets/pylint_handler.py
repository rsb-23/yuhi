import os
import subprocess
from collections import defaultdict
from operator import itemgetter
from pathlib import Path

import click

NAME_ARG_MAP = {
    "too-many-lines": "max-module-lines",
    "too-many-arguments": "max-args",
    "too-many-boolean-expressions": "max-bool-expr",
    "too-many-instance-attributes": "max-attributes",
}
PYLINT_REPORT = Path("yuhi-pylint.txt")
venv_path = Path.cwd() / "venv"


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

    unique_messages["C"]["missing-docstring"] = 0
    unique_messages["R"]["duplicate-code"] = 0
    return unique_messages, max_config


def get_config_arg(check_name):
    return NAME_ARG_MAP.get(check_name, f"max-{check_name[9:]}")


def run_in_venv(cmd: str, check=True):  # TODO: move to pkg_install.py
    env = os.environ.copy()
    env["VIRTUAL_ENV"] = str(venv_path)
    env["PATH"] = str(Path.cwd()) + env["PATH"]

    subprocess.run(cmd, env=env, check=check, shell=True)


def _run_pylint(folders=None):
    if not folders:
        folders = ["src", "test", "tests"]
    disables = ",".join(["duplicate-code", "missing-docstring"])
    sources = " ".join(f"./{fol}" for fol in folders if Path(fol).exists())

    click.echo("Running pylint...")
    run_in_venv(f"pylint {sources} -sn --enable=all --disable={disables} > {PYLINT_REPORT}", check=False)


def get_pylint_config() -> str:
    _run_pylint()
    unique_messages, max_config = _generate_report()
    config_lines = [f"{get_config_arg(name)} = {limit}\n" for name, limit in max_config.items()]
    disable_errors = "disable=\n\tI,"
    error_sep = "\n\t"
    for k, v in unique_messages.items():
        if v:
            msgs_with_count = (f"{msg}, #{count or 'keep'}" for msg, count in sorted(v.items()))
            disable_errors += f"\n\t# {k}\n\t{error_sep.join(msgs_with_count)}"
    pylint_config = f"""[MASTER]\njobs=2\nignore-paths=(?!(src|tests))/*\n
[FORMAT]\nmax-line-length = 130\n
[REFACTORING]\n{sorted(config_lines) or ""}\n
[MESSAGES CONTROL]\n{disable_errors}
"""
    return pylint_config


if __name__ == "__main__":
    pass
