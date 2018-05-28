#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_update_query(model, fields, filters):
    """
    Builds a query for supplied model
    Args:
        model:
        fields: list of one or more fields to update
        filters: required list of one or more fields to filter query

    Returns:
        valid sql statement for model
    """
    str_uf = ""
    str_uw = ""
    name = model["name"]
    fld_count = len(fields)
    whr_count = len(filters)

    # field=value part
    for idx, field in enumerate(fields):
        if (idx + 1) == fld_count:
            str_uf = str_uf + "{}=?".format(field)
        else:
            str_uf = str_uf + "{}=? , ".format(field)

    # where 'field' operator
    for idx, u_item in enumerate(filters):
        field = u_item[0]
        operator = u_item[1].upper()
        andor = ""
        if len(u_item) == 3:
            andor = u_item[2].upper()
        if (idx + 1) == whr_count:
            str_uw = str_uw + " {} {} ?".format(field, operator)
        else:
            if len(u_item) == 3:
                str_uw = str_uw + " {} {} ? {}".format(field, operator, andor)
            else:
                str_uw = str_uw + " {} {} ?".format(field, operator)

    return "UPDATE {} SET {} WHERE {};".format(name, str_uf, str_uw)
