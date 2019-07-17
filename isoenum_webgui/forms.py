#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Isotopic enumerator web interface forms.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired


class FileForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
