========
Usage
========

This library provides the Flake8 plugin ``flake8-sphinx-links``  to check docstrings for double backticked
strings which should be links to the Python documentation.


For example, \`\`True\`\` should be py\:obj:\`True\`, which Sphinx will render as a link to the Python documentation.
See :doc:`examples` for further examples.

reStructuredText .rst files are not currently checked.


Flake8 codes
--------------

.. flake8-codes:: flake8_sphinx_links

	SXL001


Pre-commit hook
----------------

``flake8-sphinx-links`` can also be used as a ``pre-commit`` hook
See `pre-commit <https://github.com/pre-commit/pre-commit>`_ for instructions

Sample ``.pre-commit-config.yaml``:

.. pre-commit:flake8:: 0.2.1
