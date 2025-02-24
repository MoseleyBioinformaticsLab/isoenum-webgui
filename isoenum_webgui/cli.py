#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The isoenum-webgui command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
    isoenum_webgui -h | --help

    isoenum_webgui --version

    isoenum_webgui [--port=<port>] [--browser] [--debug]

Options:
    -h, --help                      Show this screen.
    --version                       Show version.
    -b, --browser                   Open isoenum-webgui in a default browser.
    -p, --port=<port>               Port [default: 5000].
    --debug                         Debug mode flag.
"""

import webbrowser
import threading

from isoenum_webgui import app


def open_browser(port="5000"):
    """Open isoenum-webgui in a default browser.

    :param str port: Port number (default 5000).
    :return: None.
    :rtype: :py:obj:`None`
    """
    webbrowser.open_new("http://127.0.0.1:{}/".format(str(port)))


def cli(cmdargs):
    """Command-line interface entry point.

    :param dict cmdargs: Command-line arguments from docopt.
    :return: None.
    :rtype: :py:obj:`None`
    """
    if cmdargs["--browser"]:
        threading.Timer(0.5, open_browser, [], {"port": cmdargs["--port"]}).start()
        app.run(debug=cmdargs["--debug"], port=cmdargs["--port"])
    else:
        app.run(debug=cmdargs["--debug"], port=cmdargs["--port"])
