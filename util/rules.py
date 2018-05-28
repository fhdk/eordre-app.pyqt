#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Validation rules"""

__appname__ = "Eordre NG"
__module__ = "rules"

BC = "\033[1;36m"
EC = "\033[0;1m"
DBG = False


def printit(something):
    """
    Print something when debugging
    Args:
        something: the string to be printed
    """
    if DBG:
        print("{}\n{}{}{}".format(__module__, BC, something, EC))


def validate_fields():
    """
    Validates the QLineEdits based on RegEx
    """
    print("TODO: Create validation rules")


def check_settings(settings):
    """
    Check the vital current

    Args:
        settings: dict

    Returns:
        bool indicating if current is missing
    """
    s = settings
    printit(s)
    try:
        return bool(s["usermail"] and s["userpass"] and s["usercountry"] and
                    s["http"] and s["smtp"] and s["port"] and s["mailto"])
    except KeyError:
        return False
