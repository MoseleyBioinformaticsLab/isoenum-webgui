#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator web interface custom exception handling.
"""

from flask import Blueprint, jsonify

from ctfile.exceptions import IsotopeSpecError
from ctfile.exceptions import ChargeSpecError


errors = Blueprint("errors", __name__)


@errors.app_errorhandler(IsotopeSpecError)
@errors.app_errorhandler(ChargeSpecError)
def handle_error(error):
    message = [str(x) for x in error.args]
    status_code = 500
    success = False
    response = {
        "success": success,
        "error": {"type": error.__class__.__name__, "message": message},
    }

    return jsonify(response), status_code
