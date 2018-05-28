#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_create_query(model):
    """
    Builds a query for supplied model
    Args:
        model:

    Returns:
        valid sql statement for model
    """
    string = ""
    name = model["name"]
    fld_count = len(model["fields"])

    for idx, field_def in enumerate(zip(model["fields"], model["types"])):
        field = field_def[0]
        define = field_def[1]
        if (idx + 1) == fld_count:
            string = string + "{} {}".format(field, define)
        else:
            string = string + "{} {}, ".format(field, define)

    return "CREATE TABLE IF NOT EXISTS {} ({});".format(name, string)
