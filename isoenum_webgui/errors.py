#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum_webgui.errors
~~~~~~~~~~~~~~~~~~~~~

Isotopic enumerator web interface custom exception handling.
"""

from flask import Blueprint, jsonify

from ctfile.exceptions import IsotopeSpecError
from ctfile.exceptions import ChargeSpecError
from isoenum.exceptions import EmptyCTFileError


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(IsotopeSpecError)
@errors.app_errorhandler(ChargeSpecError)
@errors.app_errorhandler(EmptyCTFileError)
def handle_error(error):
    """Custom error handler."""
    message = [str(x) for x in error.args]
    status_code = 500
    success = False
    response = {
        "success": success,
        "error": {"type": error.__class__.__name__, "message": message},
    }

    return jsonify(response), status_code
