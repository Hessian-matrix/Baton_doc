# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
html_show_sourcelink = False

project = 'Viobot2用户手册'
# project = 'baton_doc'
copyright = '2024, hessian'
author = 'HessianMatrix'
release = '1.26'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
]

templates_path = ['_templates']
exclude_patterns = []

language = "zh_CN"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_title = 'Hessian Matrix 产品文档'
html_static_path = ['_static']
html_css_files = ['custom.css', 'product-portal.css']
html_theme_options = {
    'repository_url': '',
    'use_repository_button': False,
    'use_issues_button': False,
    'use_edit_page_button': False,
    'use_download_button': False,
    'home_page_in_toc': True,
    'show_navbar_depth': 1,
    'navbar_center': ['product-links.html'],
    'navbar_persistent': ['search-button-field'],
}

latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
'preamble': r'''
\addto\captionsenglish{\renewcommand{\chaptername}{}}
\usepackage[UTF8, scheme = plain]{ctex}
\setCJKmainfont{FandolSong-Regular.otf}
'''
}
