#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""File Functions"""

import os


def check_file(name, folder=False):
    """
    Check if file exist
    Args:
        name: 
        folder: 

    :returns bool if existing
    """
    if folder:
        return os.path.isdir(name)
    return os.path.isfile(name)


def create_dir(dirname):
    """
    Create directory if not exist
    Args:
        dirname: 
    """
    os.makedirs(dirname, mode=0o744, exist_ok=True)
