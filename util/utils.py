#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Utility module
"""

from configuration import config
from util import httpFn


def country_name_from_iso(iso):
    """
    Return country name
    Args:
        iso:
    Returns:
        Full country name
    """
    for c in config.COUNTRIES:
        if c[0] == iso:
            return c[1]


def refresh_sync_status(settings):
    """
    Refresh dates for datafiles
    Args:
        settings:
    Returns:
        Two tuples with target and date time value
    """
    return httpFn.update_last_sync_info(settings)


def arg2bool(arg):
    """
    Convert a string to bool
    Args:
        arg
    Returns:
        bool representation of the string
    """
    if type(arg) == int:
        arg = str(arg)
    return arg.lower() in ["sand", "true", "1", "ok"]


def int2bool(arg):
    """
    Convert an integer to bool
    Args:
        arg:

    Returns:
        bool representation of the integer
    """
    return arg > 0


def bool2int(arg):
    """
    Convert bool to int
    Args:
        arg:
    Returns:
        integer representation of the bool value
    """
    if arg:
        return 1
    return 0


def int2strdk(arg):
    """
    Convert bool to string
    Args:
        arg:
    Returns:
        String representation of the bool value
    """
    if arg is not 0:
        return "JA"
    return "NEJ"


def bool2dk(arg):
    """
    Convert bool to string
    Args:
        arg:
    Returns:
        String representation of the bool value
    """
    if arg:
        return "JA"
    return "NEJ"


def bool2str(arg):
    """
    Convert bool to string
    Args:
        arg:
    Returns:
        String representation of the bool value
    """
    if arg:
        return "True"
    return "False"
