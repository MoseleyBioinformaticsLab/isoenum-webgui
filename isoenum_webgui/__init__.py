#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator web interface.
"""

import json
import os

from flask import Flask
import flask_excel

from .errors import errors


__version__ = "0.1.0"

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"

RECORDS = {}

this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, "config", "example_project.json"), "r") as inf:
    EXAMPLE_PROJECT = json.load(inf)

with open(os.path.join(this_dir, "config", "header.json"), "r") as inf:
    HEADER = json.load(inf)

with open(os.path.join(this_dir, "config", "csv_header.json"), "r") as inf:
    CSV_HEADER = json.load(inf)

with open(os.path.join(this_dir, "config", "nmr_types.json"), "r") as inf:
    NMR_TYPES = json.load(inf)

app.register_blueprint(errors)
flask_excel.init_excel(app)

from isoenum_webgui import routes
