from .code_quality import add_pre_commit, add_sourcery
from .project import add_contribution, add_gitignore, add_license, add_readme

SUBGROUP_ADD = [add_contribution, add_gitignore, add_license, add_pre_commit, add_readme, add_sourcery]
SUBGROUP_CREATE = []
