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


def item_price(item, pcs):
    """
    Extract the correct price for pcs of item
    :param item:
    :param pcs:
    :return: the items price for pcs
    """
    num = int(pcs)
    if num >= 96 and item["d96"] is not 0.0:
        return item["d96"]
    if num >= 48 and item["d48"] is not 0.0:
        return item["d48"]
    if num >= 24 and item["d24"] is not 0.0:
        return item["d24"]
    if num >= 12 and item["d12"] is not 0.0:
        return item["d12"]
    if num >= 8 and item["d8"] is not 0.0:
        return item["d8"]
    if num >= 6 and item["d6"] is not 0.0:
        return item["d6"]
    if num >= 4 and item["d4"] is not 0.0:
        return item["d4"]
    if num >= 3 and item["d3"] is not 0.0:
        return item["d3"]
    if num >= 2 and item["d2"] is not 0.0:
        return item["d2"]
    return item["price"]
