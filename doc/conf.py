"""
    Configuration file for the Sphinx documentation builder.
"""

import datetime
import pathlib
import os
from typing import MutableMapping
import sphinx_rtd_theme


def get_meta() -> MutableMapping:
    """Get project metadata from pyproject.toml file.
    Returns:
        MutableMapping
    """
    import tomli

    toml_path = os.path.join(os.path.dirname(__file__), '..', 'pyproject.toml')

    with open(toml_path, mode='rb') as fopen:
        pyproject = tomli.load(fopen)

    return pyproject


print(get_meta()['project'])

date = datetime.date.today()
year = date.strftime('%Y')
pyproject_data = get_meta()
pwd = pathlib.Path(__file__).parent.resolve()

constants_sourcefile = os.path.join(pwd, '../src/wg_federation/constants.py')
constants = {'__file__': constants_sourcefile}

with open(constants_sourcefile) as constants_module:
    exec(constants_module.read(), constants)

project = pyproject_data['project']['name']
copyright = year + ', ' + pyproject_data['project']['authors'][0]['name']
author = 'Anuvu DevOps Team'
release = constants['__version__']

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]


templates_path = ['_templates']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
