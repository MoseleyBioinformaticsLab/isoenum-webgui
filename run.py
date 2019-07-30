#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The isoenum-webgui command-line interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Usage:
    run -h | --help
    run --version
    run [--port=<port>] [--browser]

Options:
    -h, --help                      Show this screen.
    --version                       Show version.
    -b, --browser                   Open default browser.
    -p, --port=<port>               Port [default: 5000].
"""

import webbrowser
import threading

import docopt

from isoenum_webgui import app
from isoenum_webgui import __version__


def open_browser(port):
    webbrowser.open_new("http://127.0.0.1:{}/".format(str(port)))


def cli(cmdargs):
    if cmdargs["--browser"]:
        threading.Timer(0.5, open_browser, [], {"port": cmdargs["--port"]}).start()
        app.run(debug=False, port=cmdargs["--port"])
    else:
        app.run(debug=False, port=cmdargs["--port"])


if __name__ == "__main__":
    cli(docopt.docopt(doc=__doc__, version=__version__))
