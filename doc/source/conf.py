# -*- coding: utf-8 -*-
#

import sys, os
sys.path.insert(0, os.path.abspath('../..'))

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest']
templates_path = []
source_suffix = '.rst'
master_doc = 'index'

project = 'roboball2d'
copyright = '(C) 2020, Max Planck Gesellschaft'

with open(os.path.join(os.path.dirname(__file__),"..", "..", 'VERSION')) as fd:
    VERSION = fd.readline().strip()
version = VERSION
release = VERSION

exclude_trees = ['build']
pygments_style = 'sphinx'

html_theme = 'sphinx_rtd_theme'
html_theme_options = {}

html_static_path = []
htmlhelp_basename = 'roboball2ddoc'

latex_documents = [
  ('index', 'roboball2d.tex', ur'Roboball2d Documentation',
   ur'Nicolas Guetler and Vincent Berenz', 'manual'),
]

