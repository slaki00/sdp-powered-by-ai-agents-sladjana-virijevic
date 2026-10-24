"""Sphinx configuration file for Kata documentation."""

# -- Project information -----------------------------------------------------
project = "BankOCR"
copyright = "2026, Sladjana Virijevic"
author = "Sladjana Virijevic"
release = "1.0.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_wagtail_theme",
    "myst_parser",
    "sphinx_new_tab_link",
]

new_tab_link_show_external_link_icon = True

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_wagtail_theme"

html_theme_options = {
    "project_name": "BankOCR",
    "github_url": "https://github.com/slaki00/sdp-powered-by-ai-agents-sladjana-virijevic",
    "footer_links": "",
}

html_show_copyright = True
html_last_updated_fmt = "%b %d, %Y"
html_show_sphinx = False

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "tasklist",
]
