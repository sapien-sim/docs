project = 'sapien'
author = 'SAPIEN-TEAM'
release = "3.0"
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
    "sphinx_copybutton",
    "myst_parser",
    "sphinx_design",
    "sphinx_subfigure",
]
todo_include_todos = True
source_suffix = ['.rst', '.md']
source_parsers = {
    '.md': 'recommonmark.parser.CommonMarkParser',
}
master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']

html_context = {
    "display_github": True,
    "github_user": "sapien-sim",
    "github_repo": "docs",
    "github_version": "main",
    "conf_py_path": "docs/source/"
}

html_theme_options = {
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/sapien-sim/docs",
            "icon": "fa-brands fa-github",
        }
    ],
}
myst_enable_extensions = {
    "colon_fence"
}
