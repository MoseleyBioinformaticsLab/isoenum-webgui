#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator web interface routes.
"""

import collections
import csv
import io
import json

from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import flash
from pyexcel.exceptions import FileTypeNotSupported

from isoenum_webgui import app
from isoenum_webgui.forms import FileForm
from isoenum_webgui.proc import generate_table
from isoenum_webgui.proc import generate_nmr
from isoenum_webgui.proc import update_record
from isoenum_webgui.proc import create_initial_record
from isoenum_webgui.proc import create_empty_record

from . import NMR_DATA
from . import RECORDS
from . import HEADER
from . import CSV_HEADER
from . import EXAMPLE_PROJECT


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    file_input_form = FileForm()
    if file_input_form.validate_on_submit():
        if RECORDS:
            RECORDS.clear()

        try:
            json_str = request.files["file"].read()
            RECORDS.update(json.loads(json_str))

        except json.decoder.JSONDecodeError:

            try:
                table_data = request.get_array(field_name="file")
                table_header = table_data.pop(0)

                for table_row in table_data:
                    record = create_initial_record(header=table_header, row=table_row)
                    RECORDS[record["record_id"]] = record

                for i in generate_table(records=RECORDS):
                    progress_percentage = "{0:.0%}".format(i / len(RECORDS))
                    print(progress_percentage)

            except FileTypeNotSupported:
                flash("Invalid file", "danger")
                return render_template("home.html", file_input_form=file_input_form)

        except Exception:
            flash("Invalid file", "danger")
            return render_template("home.html", file_input_form=file_input_form)

        return redirect(url_for("table"))
    return render_template("home.html", file_input_form=file_input_form)


@app.route("/example", methods=["GET", "POST"])
def example_project():
    if RECORDS:
        RECORDS.clear()
    RECORDS.update(EXAMPLE_PROJECT)
    return redirect(url_for("table"))


@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "POST" and request.form.get("nmr-inchi-table-data"):
        nmr_experiment_type = request.form.get("select-nmr-experiment")
        generate_nmr(nmr_experiment_type=nmr_experiment_type, nmr_data=NMR_DATA, records=RECORDS)
        return redirect(url_for("nmrtable", nmr_type=nmr_experiment_type))

    return render_template("table.html", table_header=HEADER, table_data=RECORDS)


@app.route("/nmrtable", methods=["GET", "POST"])
def nmrtable():
    if request.method == "POST" and request.form.get("go-back-button"):
        return redirect(url_for("table"))

    if request.method == "POST" and request.form.get("export-zip"):
        return redirect(url_for("export", cpd=request.args.get("cpd")))

    if request.method == "POST" and request.form.get("save-csv"):
        docs = json.loads(
            request.form.get("final-table-data-csv"),
            object_pairs_hook=collections.OrderedDict,
        )
        return redirect(url_for("download_csv"))

    if request.method == "POST" and request.form.get("save-json"):
        docs = json.loads(
            request.form.get("final-table-data-json"),
            object_pairs_hook=collections.OrderedDict,
        )
        return redirect(url_for("download_json"))

    nmr_experiment_type = request.args.get("nmr_type", "1D-1H")

    return render_template(
        "nmrtable.html",
        table_header=HEADER,
        table_data=RECORDS,
        nmr_table_data=NMR_DATA,
        nmr_experiment_type=nmr_experiment_type,
    )


@app.route("/update_record", methods=["POST"])
def update():
    record_id = request.form.get("record_id", "")
    new_record = update_record(record=request.form)
    RECORDS[record_id].update(new_record)
    return jsonify(RECORDS[record_id])


@app.route("/add_record", methods=["POST"])
def add():
    record = create_empty_record()
    RECORDS[record["record_id"]] = record
    return jsonify({"record_id": record["record_id"]})


@app.route("/remove_record", methods=["POST"])
def remove():
    record_id = request.form.get("record_id", "")
    if record_id:
        try:
            RECORDS.pop(record_id)
        except KeyError:
            raise KeyError
    else:
        raise KeyError

    return jsonify({"record_id": record_id, "success": True})


@app.route("/molfile/<record_id>/<record_type>", methods=["GET"])
def display_molfile(record_id, record_type):
    if record_type == "repr":
        svg = RECORDS[record_id]["Repr SVG"]
        molfile = RECORDS[record_id]["Repr Molfile"]
    elif record_type == "base":
        svg = RECORDS[record_id]["Base SVG"]
        molfile = RECORDS[record_id]["Base Molfile"]
    else:
        raise ValueError("Unknown record type")
    return render_template("molfile.html", svg=svg, molfile=molfile)


@app.route("/export_json", methods=['GET'])
def export_json():
    response = app.response_class(response=json.dumps(RECORDS),
                                  status=201,
                                  mimetype="application/json",
                                  headers={"Content-Disposition": "attachment;filename=records.json"})
    return response


@app.route("/export_csv", methods=['GET'])
def export_csv():
    textio = io.StringIO()
    csv_writer = csv.writer(textio)
    header = CSV_HEADER["table"]
    csv_writer.writerow(header)

    for record in RECORDS.values():
        row = [record[title] for title in header]
        csv_writer.writerow(row)

    response = app.response_class(response=textio.getvalue(),
                                  status=201,
                                  mimetype="text/csv",
                                  headers={"Content-Disposition": "attachment;filename=records.csv"})
    return response

