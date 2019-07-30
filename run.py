#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
run script to start isoenum-webgui interface in development mode.

Example:
    $ python run.py --debug
"""


import docopt

from isoenum_webgui import cli
from isoenum_webgui import __version__


if __name__ == "__main__":
    cli.cli(docopt.docopt(doc=cli.__doc__, version=__version__))
