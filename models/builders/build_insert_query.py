#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_insert_query(model):
    """
    Builds a query for supplied model
    Args:
        model:

    Returns:
        valid sql statement for model
    """
    name = model["name"]
    fld_count = len(model["fields"])
    stringf = ""
    stringv = ""
    for idx, field in enumerate(model["fields"]):
        if (idx + 1) == fld_count:
            stringf = stringf + field
            stringv = stringv + "?"
        else:
            stringf = stringf + field + ","
            stringv = stringv + "?,"
    return "INSERT INTO {} ({}) VALUES ({});".format(name, stringf, stringv)
