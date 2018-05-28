#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Configuration functions"""

from util import fileFn

from . import config


def check_config_folder():
    """Checks if the APP_DATA folder exist and creates if not"""
    if not fileFn.check_file(config.APP_DATA, folder=True):
        fileFn.create_dir(config.APP_DATA)
