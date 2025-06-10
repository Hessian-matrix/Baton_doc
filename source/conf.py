# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'
html_show_sourcelink = False

project = 'Viobot2用户手册'
# project = 'baton_doc'
copyright = '2024, hessian'
author = 'HessianMatrix'
release = '1.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'recommonmark',
    'sphinx_markdown_tables',
    'sphinx_rtd_theme'
]

templates_path = ['_templates']
exclude_patterns = []

language = "ch"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

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