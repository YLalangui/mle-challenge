import re
from pathlib import Path

RELEASE_PAT = r'version = \"(.*)\"'

project = 'mle-challenge'
author = 'Yerhard Lalangui Fernandez'

with open(Path(__file__).parent.parent.parent / 'pyproject.toml') as f:
    release = re.search(RELEASE_PAT, f.read()).groups()[0]

extensions = ['sphinxcontrib.napoleon', 'myst_parser']

templates_path = ['_templates']

exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
