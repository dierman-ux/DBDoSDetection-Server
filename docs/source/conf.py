import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath('../../server'))
sys.path.insert(0, os.path.abspath('../../client'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'blacklist_server'
copyright = '2025, Rafael Malla Martinez'
author = 'Rafael Malla Martinez'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [    
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    ]

templates_path = ['_templates']
exclude_patterns = []

language = 'y'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        return MagicMock()

MOCK_MODULES = ['http_handler', 'server', 'detection']  # módulos que fallan al importar

for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()
