#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
isoenum_webgui.config
~~~~~~~~~~~~~~~~~~~~~


This module contains `isoenum-webgui` application configurations.
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Set `isoenum-webgui` Flask app configuration."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    ENV = os.environ.get("FLASK_ENV") or "development"
