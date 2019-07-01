import json
import os

from flask import Flask
import flask_excel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

RECORDS = {}
NMR_DATA = {}

this_dir = os.path.dirname(__file__)
with open(os.path.join(this_dir, "config", "example_project.json"), "r") as inf:
    example_project = json.load(inf)

with open(os.path.join(this_dir, "config", "header.json"), "r") as inf:
    HEADER = json.load(inf)

flask_excel.init_excel(app)

from isoenum_webgui import routes
