import uuid
import re

from flask import url_for
import isoenum

from . import HEADER
from . import NMR_TYPES


def generate_repr_molfile(inchi_str, iso_str, chg_str):
    """

    :param inchi_str:
    :param iso_str:
    :param chg_str:
    :return:
    """
    molfile = isoenum.fileio.create_ctfile(inchi_str)

    if iso_str:
        for iso_spec in iso_str.split(","):
            try:
                isotope, atom_symbol, atom_number = iso_spec.split(":")
            except:
                raise ValueError(
                    "Incorrect isotope specification, use <isotope:element:position> format,"
                    "e.g. 13:C:1"
                )

            molfile.add_iso(
                atom_symbol=atom_symbol, atom_number=atom_number, isotope=isotope
            )

    if chg_str:
        for chg_spec in chg_str.split(","):
            try:
                atom_symbol, atom_number, charge = chg_spec.split(":")
            except:
                raise ValueError(
                    "Incorrect charge specification, use <element:position:charge> format,"
                    "e.g. O:4:-1"
                )
            molfile.add_chg(
                atom_symbol=atom_symbol, atom_number=atom_number, charge=charge
            )
    return molfile


def generate_table(records):
    """

    :param records:
    :return:
    """
    for index, record in enumerate(records.values(), start=1):
        repr_record = update_record(record=record)
        record.update(repr_record)
        yield index


def create_initial_record(header, row):
    """

    :return:
    """
    record = create_empty_record()
    record.update(dict(zip(header, row)))
    return record


def update_record(record):
    """

    :param inchi_str:
    :param iso_str:
    :param chg_str:
    :return:
    """
    record_inchi_str = record["Base Identifier"]
    record_iso_str = record["ISO"]
    record_chg_str = record["CHG"]
    record_id = record["record_id"]

    iso_pattern = re.compile("\d+:[a-zA-z]{1,2}:\d+")
    chg_pattern = re.compile("[a-zA-Z]{1,2}:\d+:[+-]\d+")

    iso_list = re.findall(iso_pattern, record_iso_str)
    chg_list = re.findall(chg_pattern, record_chg_str)

    try:
        base_molfile = isoenum.fileio.create_ctfile(record_inchi_str)

        base_molfile_iso = [
            (atom.isotope, atom.atom_symbol, atom.atom_number)
            for atom in base_molfile.atoms
            if atom.isotope
        ]

        base_molfile_chg = [
            (atom.atom_symbol, atom.atom_number, atom.charge)
            for atom in base_molfile.atoms
            if atom.charge != "0"
        ]

        if base_molfile_iso or base_molfile_chg:
            for iso in base_molfile_iso:
                _, atom_symbol, atom_number = iso
                iso_list.append(":".join(iso))
                base_molfile.remove_iso(
                    atom_symbol=atom_symbol, atom_number=atom_number
                )

            for chg in base_molfile_chg:
                atom_symbol, atom_number, _ = chg
                chg_list.append(":".join(chg))
                base_molfile.remove_chg(
                    atom_symbol=atom_symbol, atom_number=atom_number
                )

        record_inchi_str = isoenum.fileio.create_inchi_from_ctfile_obj(base_molfile)
        base_molfile_str = base_molfile.writestr(file_format="ctfile")

        base_svg_str = create_svg(inchi_str=record_inchi_str)
        base_svg_link = create_svg_link(
            svg_str=base_svg_str, record_id=record_id, record_type="base"
        )

        iso_str = ",".join(iso_list)
        chg_str = ",".join(chg_list)

        repr_inchi_str = create_repr_inchi(
            base_inchi_str=record_inchi_str, iso_str=iso_str, chg_str=chg_str
        )
        repr_molfile = isoenum.fileio.create_ctfile(repr_inchi_str)
        repr_molfile_str = repr_molfile.writestr(file_format="ctfile")
        repr_svg_str = create_svg(inchi_str=repr_inchi_str)
        repr_svg_link = create_svg_link(
            svg_str=repr_svg_str, record_id=record_id, record_type="repr"
        )

        html_iso_str = "<br>".join(iso_list)
        html_chg_str = "<br>".join(chg_list)

        record = {
            "Base Identifier": record_inchi_str,
            "Base SVG Str": base_svg_str,
            "Base SVG": base_svg_link,
            "Base Molfile": base_molfile_str,
            "Repr Identifier": repr_inchi_str,
            "Repr SVG Str": repr_svg_str,
            "Repr SVG": repr_svg_link,
            "Repr Molfile": repr_molfile_str,
            "ISO": html_iso_str,
            "CHG": html_chg_str,
            "error_message": "",
        }
    except ValueError as err:
        error_message = " ".join(err.args)
        record = {
            "Base Identifier": record_inchi_str,
            "Base SVG Str": "",
            "Base SVG": "",
            "Base Molfile": "",
            "Repr Identifier": "",
            "Repr SVG Str": "",
            "Repr SVG": "",
            "Repr Molfile": "",
            "ISO": "",
            "CHG": "",
            "error_message": error_message,
        }

    return record


def create_repr_inchi(base_inchi_str, chg_str, iso_str):
    repr_molfile = generate_repr_molfile(
        inchi_str=base_inchi_str, iso_str=iso_str, chg_str=chg_str
    )
    repr_inchi_str = isoenum.fileio.create_inchi_from_ctfile_obj(repr_molfile)
    return repr_inchi_str


def create_svg(inchi_str):
    svg_str = isoenum.fileio.create_svg_str(
        inchi_str, xH="-xH", xe="-xe", xi="-xi", bg="-xb none"
    )
    return svg_str


def create_svg_link(svg_str, record_id, record_type):
    """

    :param svg_str:
    :return:
    :rtype:
    """
    svg_link = '<a href="{}" target="_blank">{}</a>'.format(
        url_for("display_molfile", record_id=record_id, record_type=record_type),
        svg_str,
    )
    return svg_link


def generate_nmr(nmr_experiment_type, nmr_data, records):
    """

    :param nmr_experiment_type:
    :param nmr_data:
    :param records:
    :return:
    """
    nmr_data.setdefault(nmr_experiment_type, {})
    nmr_experiment_type = NMR_TYPES[nmr_experiment_type]

    for record in records.values():
        repr_inchi = record["Repr Identifier"]

        record.setdefault("NMR", {})
        record["NMR"].setdefault(nmr_experiment_type, {})
        record["NMR"][nmr_experiment_type].setdefault(repr_inchi, [])

        if not record["NMR"][nmr_experiment_type][repr_inchi]:
            sdfile = isoenum.api.iso_nmr(
                path_or_id=repr_inchi,
                experiment_type=nmr_experiment_type,
                couplings=[],
                decoupled=[],
                subset=False,
            )

            for data in sdfile.sdfdata:
                coupling_type = data["CouplingType"]
                nmr_inchi = data["InChI"][0]
                me_group = data["MEGroup"][0]

                record["NMR"][nmr_experiment_type][repr_inchi].append(
                    {"descr": coupling_type, "inchi": nmr_inchi, "me_group": me_group}
                )
        else:
            continue


def create_record_id():
    """Create record id.

    :return: Record id string.
    :rtype: str
    """
    return str(uuid.uuid4())


def create_empty_record():
    """Create empty record.

    :return: Empty record dictionary.
    :rtype: dict
    """
    record_id = create_record_id()
    empty_record = {}
    for col in HEADER:
        if col["title"] == "record_id":
            empty_record[col["title"]] = record_id
        else:
            empty_record[col["title"]] = ""
    return empty_record
