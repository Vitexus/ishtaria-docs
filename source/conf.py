# Sphinx configuration for the Ishtaria documentation.

project = "Ishtaria"
author = "Vítězslav Dvořák and contributors"
copyright = "2026, Vítězslav Dvořák / VitexSoftware (CC BY-SA 4.0)"
release = "0.1"
version = "0.1"

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.graphviz",
]

language = "en"
locale_dirs = ["../locale/"]   # Czech translation via sphinx-intl
gettext_compact = False

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_title = "Ishtaria documentation"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_favicon = "_static/favicon.ico"
html_theme_options = {
    "navigation_depth": 3,
    "collapse_navigation": False,
}
html_context = {
    "display_github": False,
    "github_user": "VitexSoftware",
    "github_repo": "ishtaria-docs",
    "github_version": "main",
    "conf_py_path": "/source/",
}

todo_include_todos = True
graphviz_output_format = "svg"
