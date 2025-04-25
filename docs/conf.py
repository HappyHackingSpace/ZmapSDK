# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import tomlkit


def _get_project_details():
    """Get project meta details."""
    with open("../pyproject.toml") as pyproject:
        content = pyproject.read()

    return tomlkit.parse(content)["project"]


pkg_meta = _get_project_details()
project = str(pkg_meta["name"])
version = str(pkg_meta["version"])
copyright = "2025, Happy Hacking Space"
author = "Happy Hacking Space"
release = version


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
autoclass_content = "class"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "autoapi.extension",
]

master_doc = "index"

# autoapi
autoapi_dirs = ["../../zmapsdk/"]
autoapi_type = "python"
templates_path = ["_templates"]
exclude_patterns = [".DS_Store", "_build", "Thumbs.db"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
