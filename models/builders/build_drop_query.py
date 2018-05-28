#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_drop_query(model):
    """
    Builds a query for supplied model
    Args:
        model:

    Returns:
        valid sql statement for model
    """
    name = model["name"]

    return "DROP TABLE IF EXISTS {};".format(name)
