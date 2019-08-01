#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum_webgui.forms
~~~~~~~~~~~~~~~~~~~~

Isotopic enumerator web interface forms.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class FileForm(FlaskForm):
    """File input form with validation."""

    file = FileField(validators=[FileRequired()])
