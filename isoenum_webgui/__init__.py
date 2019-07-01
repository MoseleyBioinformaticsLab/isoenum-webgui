import json
import os

from flask import Flask
import flask_excel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, "config", "example_project.json"), "r") as inf:
    example_project = json.load(inf)

RECORDS = {}
NMR_DATA = {}
HEADER = [
    {"title": "Name", "editable": True, "hidden": False},
    {"title": "Base Identifier", "editable": True, "hidden": False},
    {"title": "Base SVG Str", "editable": False, "hidden": True},
    {"title": "Base SVG", "editable": False, "hidden": False},
    {"title": "Base Molfile", "editable": False, "hidden": True},
    {"title": "ISO", "editable": True, "hidden": False},
    {"title": "CHG", "editable": True, "hidden": False},
    {"title": "Repr Identifier", "editable": False, "hidden": False},
    {"title": "Repr SVG Str", "editable": False, "hidden": True},
    {"title": "Repr SVG", "editable": False, "hidden": False},
    {"title": "Repr Molfile", "editable": False, "hidden": True},
    {"title": "record_id", "editable": False, "hidden": True},
]


flask_excel.init_excel(app)

from isoenum_webgui import routes
