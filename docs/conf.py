# -*- coding: utf-8 -*-
#
# project test documentation build configuration file, created by
# sphinx-quickstart on Tue Jan 19 19:30:57 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import os.path
import sys

file_path = os.path.abspath(__file__)
sys.path.insert(0, os.path.dirname(os.path.dirname(file_path)))

from docs import _build_configs_

# import sphinx_wagtail_theme

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# sys.path.insert(0, os.path.abspath('.'))
PROJECT_FINAL_NAME = "KASPERS APIS"
PROJECT_COPYRIGHT = "2021, Kasper de Bruin"
PROJECT_AUTHOR = "Kasper de Bruin"

# Generate the HTML in the sphinx folder so it will be made
# available in read the docs
commit = '0.1'

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    "breathe"
]

# Breathe Configuration

breathe_default_members = (
    "members",
    "protected-members",
    "private-members",
    "undoc-members",
)

breathe_doxygen_aliases = {
    'rstref{1}': r'\verbatim embed:rst:inline :ref:`\1` \endverbatim'
}

breathe_show_include = True
breathe_show_define_initializer = True
breathe_show_enumvalue_initializer = True

breathe_domain_by_extension = {
    "usf": "cpp",
}

breath_source_projects_source = "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/generated/doxygen"

breathe_projects = {
    "KdsCharacter": f"{breath_source_projects_source}/KdsCharacter/KdsCharacter/xml",
    "KdsEditorModule": f"{breath_source_projects_source}/KdsCharacter/KdsEditorModule/xml",

    "ALS": f"{breath_source_projects_source}/ALS/ALS/xml",
    "ALSCamera": f"{breath_source_projects_source}/ALS/ALSCamera/xml",
    "ALSEditor": f"{breath_source_projects_source}/ALS/ALSEditor/xml",
    "ALSExtras": f"{breath_source_projects_source}/ALS/ALSExtras/xml",

    "KdsEditorPlugin": f"{breath_source_projects_source}/KdsEditorPlugin/KdsEditorPlugin/xml",
    "KdsLogging": f"{breath_source_projects_source}/KdsLogging/KdsLogging/xml",
    "KdsMacroLib": f"{breath_source_projects_source}/KdsMacroLib/KdsMacroLib/xml",

    "RiderLink": f"{breath_source_projects_source}/RiderLink/RiderLink/xml",
    "RiderBlueprint": f"{breath_source_projects_source}/RiderLink/RiderBlueprint/xml",
    "RiderGameControl": f"{breath_source_projects_source}/RiderLink/RiderGameControl/xml",
}

breathe_default_project = "ALS"

# Tell sphinx what the primary language being documented is.
primary_domain = "cpp"

# Tell sphinx what the pygments highlight language should be.
highlight_language = "cpp"

# =================

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = "index"

# General information about the project.
project = PROJECT_FINAL_NAME
copyright = PROJECT_COPYRIGHT
author = PROJECT_AUTHOR

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = commit
# The full version, including alpha/beta/rc tags.
release = commit

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '**/pptree.py', '_build_configs_']

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output ----------------------------------------------
# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = f"{PROJECT_FINAL_NAME} v{commit}"
# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = f"{PROJECT_FINAL_NAME} v{commit}"
# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = f"_static/nf-logo-120x120.png"

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
# html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

html_theme = _build_configs_.CURRENT_THEME.theme_name
html_theme_options = _build_configs_.CURRENT_THEME.theme_options
html_css_files = _build_configs_.CURRENT_THEME.custom_css
html_context = _build_configs_.CURRENT_THEME.html_context
html_show_copyright = _build_configs_.CURRENT_THEME.show_copyright

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path =

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = f"{PROJECT_FINAL_NAME}doc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"{PROJECT_FINAL_NAME}.tex",
        f"{PROJECT_FINAL_NAME} Documentation",
        "Pierre Delaunay",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        f"{PROJECT_FINAL_NAME}",
        f"{PROJECT_FINAL_NAME} Documentation",
        [author],
        1,
    )
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        f"{PROJECT_FINAL_NAME}",
        f"{PROJECT_FINAL_NAME} Documentation",
        author,
        f"{PROJECT_FINAL_NAME}",
        f"Unreal Engine {PROJECT_FINAL_NAME}",
        "Miscellaneous",
    ),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False

# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# sphinx_tools documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
#
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# How to document -- sources:
#
#    1. `Numpy Standard <https://numpydoc.readthedocs.io/en/latest/format.html>`_
#    2. `Python Standard <https://docs.python.org/devguide/documenting.html>`_
#    3. `reST general <http://www.sphinx-doc.org/en/stable/rest.html>`_
#    4. `reST reference tags <http://www.sphinx-doc.org/en/stable/domains.html#the-python-domain>`_
#    5. `Cross-reference <http://www.sphinx-doc.org/en/stable/domains.html#python-roles>`_
#
# """
# import glob
# import os
# import re
# import sys
# import sys; sys.setrecursionlimit(1500)
# import sphinx_wagtail_theme
#
# docs_src_path = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, docs_src_path)
# src_path = os.path.abspath(os.path.join(docs_src_path, '..', 'sphinx_tools'))
# sys.path.insert(0, src_path)
# src_path = os.path.abspath(os.path.join(docs_src_path, '..'))
# sys.path.insert(0, src_path)
#
# import sphinx_tools
#
# # -- General configuration ------------------------------------------------
#
# # If your documentation needs a minimal Sphinx version, state it here.
# #
# # needs_sphinx = '1.0'
#
# # Add any Sphinx extension module names here, as strings. They can be
# # extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# # ones.
# extensions = [
#     "sphinx.ext.doctest",
#     "sphinx.ext.coverage",
#     "sphinx.ext.mathjax",
#     "breathe",
#     "exhale",
# ]
#
# autodoc_inherit_docstrings = True
#
# # General information about the project.
# project = u'KdsCharacter'
# _full_version = sphinx_tools.__version__
# author = sphinx_tools.__author__
# copyright = sphinx_tools.__copyright__
#
# # The version info for the project you're documenting, acts as replacement for
# # |version| and |release|, also used in various other places throughout the
# # built documents.
# #
# # The full version, including alpha/beta/rc tags.
# release = re.sub(r'(.*?)(?:\.dev\d+)?(?:\+.*)?', r'\1', _full_version)
# # The short X.Y version.
# version = re.sub(r'(\d+)(\.\d+)?(?:\.\d+)?(?:-.*)?(?:\.post\d+)?', r'\1\2', release)
#
# breathe_projects = {
#     "ALS": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/ALS/ALS/xml",
#     "Developer": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/Developer/Developer/xml",
#     "KantanDocGenPlugin": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/KantanDocGenPlugin/KantanDocGenPlugin/xml",
#     "KdsCharacter": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/KdsCharacter/KdsCharacter/xml",
#     "KdsEditorPlugin": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/KdsEditorPlugin/KdsEditorPlugin/xml",
#     "KdsLogging": "E:/_00_blackdog/Docs/TestDocProject/Tools/sphinx_tools/docs/KdsLogging/KdsLogging/xml"
# }
#
#
# # The suffix(es) of source filenames.
# # You can specify multiple suffix as a list of string:
# #
# # source_suffix = ['.rst', '.md']
# source_suffix = '.rst'
#
# # The master toctree document.
# master_doc = 'index'
#
# # The language for content autogenerated by Sphinx. Refer to documentation
# # for a list of supported languages.
# #
# # This is also used if you do content translation via gettext catalogs.
# # Usually you set "language" from the command line for these cases.
# language = 'en'
#
# # Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']
#
# # List of patterns, relative to source directory, that match files and
# # directories to ignore when looking for source files.
# # This patterns also effect to html_static_path and html_extra_path
#
#
# # The name of the Pygments (syntax highlighting) style to use.
# pygments_style = 'sphinx'
#
# # If true, `todo` and `todoList` produce output, else they produce nothing.
# todo_include_todos = True
#
# # The reST default role (used for this markup: `text`) to use for all documents.
# default_role = "autolink"
#
# breathe_domain_by_extension = {
#     "usf": "cpp",
# }
#
#
# breathe_default_members = (
#     "members",
#     "undoc-members",
#     "protected-members",
#     "private-member",
# )
#
# # Tell sphinx what the primary language being documented is.
# primary_domain = "cpp"
#
# # Tell sphinx what the pygments highlight language should be.
# highlight_language = "cpp"
#
#
# # -- Options for HTML output ----------------------------------------------
#
# # The theme to use for HTML and HTML Help pages.  See the documentation for
# # a list of builtin themes.
# #
# #html_theme = 'sphinx_rtd_theme'
# html_theme = "sphinx_wagtail_theme"
#
# html_theme_options = {
# }
#
# # Theme options are theme-specific and customize the look and feel of a theme
# # further.  For a list of options available for each theme, see the
# # documentation.
# #
# # html_theme_options = {}
#
# html_theme_path = [sphinx_wagtail_theme.get_html_theme_path()]
#
# # Add any paths that contain custom static files (such as style sheets) here,
# # relative to this directory. They are copied after the builtin static files,
# # so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']
#
# # Custom sidebar templates, must be a dictionary that maps document names
# # to template names.
# #
# # This is required for the alabaster theme
# # refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#     '**': [
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#     ]
# }
#
#
# # -- Options for HTMLHelp output ------------------------------------------
#
# # Output file base name for HTML help builder.
# htmlhelp_basename = 'sphinx-tools-doc'
#
#
# # -- Options for LaTeX output ---------------------------------------------
#
# latex_elements = {
#     # The paper size ('letterpaper' or 'a4paper').
#     #
#     # 'papersize': 'letterpaper',
#
#     # The font size ('10pt', '11pt' or '12pt').
#     #
#     # 'pointsize': '10pt',
#
#     # Additional stuff for the LaTeX preamble.
#     #
#     # 'preamble': '',
#
#     # Latex figure (float) alignment
#     #
#     # 'figure_align': 'htbp',
# }
#
# # Grouping the document tree into LaTeX files. List of tuples
# # (source start file, target name, title,
# #  author, documentclass [howto, manual, or own class]).
# latex_documents = [
#     (master_doc, 'sphinx-tools.tex', u'sphinx-tools Documentation',
#      u'authors', 'manual'),
# ]
#
#
# # -- Options for manual page output ---------------------------------------
#
# # One entry per manual page. List of tuples
# # (source start file, name, description, authors, manual section).
# man_pages = [
#     (master_doc, 'sphinx-tools', 'sphinx-tools Documentation',
#      [author], 1)
# ]
#
#
# # -- Options for Texinfo output -------------------------------------------
#
# # Grouping the document tree into Texinfo files. List of tuples
# # (source start file, target name, title, author,
# #  dir menu entry, description, category)
# texinfo_documents = [
#     (master_doc, 'sphinx-tools', 'sphinx-tools Documentation',
#      author, 'sphinx-tools', sphinx_tools.__descr__,
#      'Miscellaneous'),
# ]
#
# # -- Autodoc configuration -----------------------------------------------
#
# autodoc_mock_imports = ['_version', 'utils._appdirs']
#
# ################################################################################
# #                             Numpy Doc Extension                              #
# ################################################################################
#
# # sphinx.ext.autosummary will automatically be loaded as well. So:
# autosummary_generate = glob.glob("reference/*.rst")
#
# # Generate ``plot::`` for ``Examples`` sections which contain matplotlib
# numpydoc_use_plots = False
#
# # Create a Sphinx table of contents for the lists of class methods and
# # attributes. If a table of contents is made, Sphinx expects each entry to have
# # a separate page.
# numpydoc_class_members_toctree = False
