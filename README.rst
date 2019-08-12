
isoenum-webgui
==============


.. image:: https://img.shields.io/pypi/l/isoenum.svg
   :target: https://choosealicense.com/licenses/bsd-3-clause-clear
   :alt: License information


.. image:: https://readthedocs.org/projects/isoenum-webgui/badge/?version=latest
   :target: https://isoenum-webgui.readthedocs.io
   :alt: Documentation Status


.. image:: https://img.shields.io/pypi/v/isoenum-webgui.svg
   :target: https://pypi.org/project/isoenum-webgui
   :alt: Current library version


.. image:: https://img.shields.io/pypi/pyversions/isoenum-webgui.svg
   :target: https://pypi.org/project/isoenum-webgui
   :alt: Supported Python versions


``isoenum-webgui`` provides Flask-based web user interface that uses ``isoenum`` package
to generate accurate InChI (\ `International Chemical Identifier <https://www.inchi-trust.org/>`_\ ) 
for metabolites based on standard NMR experiments descriptions (currently ``1D-1H`` and 
``1D-CHSQC``\ ) in order to improve data reusability of metabolomics data.

Links
~~~~~


* isoenum @ `GitHub <https://github.com/MoseleyBioinformaticsLab/isoenum-webgui>`_
* isoenum @ `PyPI <https://pypi.org/project/isoenum-webgui>`_
* isoenum @ `ReadTheDocs <http://isoenum-webgui.readthedocs.io>`_

Installation
~~~~~~~~~~~~

The ``isoenum-webgui`` package runs under Python 3.4+. Use `pip <https://pip.pypa.io>`_ to install.

Install on Linux, Mac OS X
--------------------------

.. code-block::

   python3 -m pip install isoenum-webgui

Install on Windows
------------------

.. code-block::

   py -3 -m pip install isoenum-webgui

Dependencies
------------

The ``isoenum-webgui`` requires a **non-pip-installable** dependency: the
`Open Babel <http://openbabel.org>`_ chemistry library version 2.4.1 or later,
which relies on ``InChI`` `library <https://www.inchi-trust.org/downloads>`_ 
version 1.0.4 or later to perform ``InChI`` conversions.

Refer to the official documentation to install `Open Babel <http://openbabel.org>`_ on your system:


* Official Installation Instructions: http://openbabel.org/wiki/Category:Installation

Development version installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install development version on Linux, Mac OS X
----------------------------------------------

.. code-block::

   python3 -m pip install git+git://github.com/MoseleyBioinformaticsLab/isoenum-webgui.git

Install development version on Windows
--------------------------------------

.. code-block::

   py -3 -m pip install git+git://github.com/MoseleyBioinformaticsLab/isoenum-webgui.git

License
~~~~~~~

This package is distributed under the `BSD <https://choosealicense.com/licenses/bsd-3-clause-clear>`_ license.
