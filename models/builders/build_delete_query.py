#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_delete_query(model, filters):
    """
    Builds a query for supplied model
    Args:
        model:
        filters: required list of one or more fields to filter on

    Returns:
        valid sql statement for model
    """
    name = model["name"]
    whr_count = len(filters)
    string = ""
    # where 'field' operator
    for idx, d_item in enumerate(filters):
        field = d_item[0]
        operator = d_item[1].upper()
        andor = ""
        if len(d_item) == 3:
            andor = d_item[2].upper()
        if (idx + 1) == whr_count:
            string = string + " {} {} ?".format(field, operator)
        else:
            if andor:
                string = string + " {} {} ? {}".format(field, operator, andor)
            else:
                string = string + " {} {} ?".format(field, operator)

    return "DELETE FROM {} WHERE {};".format(name, string)
