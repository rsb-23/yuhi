# sphinx config for documentation
# pylint: disable=invalid-name

project = "Yuhi (यूँ ही)"
description = "Python CLI toolkit to automate project enhancement using standard config templates."
authors = "Rishabh B"
version = "0.1.0"
project_copyright = "%Y, Rishabh B"

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "alabaster"

html_theme_options = {
    "github_user": "rsb-23",
    "github_repo": "yuhi",
    "github_type": "star",
    "github_button": "true",
    "github_count": "true",
}

html_static_path = ["_static"]
