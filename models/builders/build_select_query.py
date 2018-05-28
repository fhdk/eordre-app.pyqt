#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


def build_select_query(model, selection=None, aggregates=None, filters=None, orderby=None):
    """
    Builds a query for supplied model
    Args:
        model:
        selection: optional list of fields to return
        aggregates: optional list of one or more valid aggregates
        filters: optional list of one or more fields to filter query
        orderby: optional sort_order

    Returns:
        valid sql statement for model
    """
    # table selection
    # the field order cannot be guaranteed with * alias
    # so we use a list of field names either the model or user supplied
    fields = model["fields"]
    if selection:
        fields = selection
    name = model["name"]
    field_count = len(fields)
    aggregate_count = 0
    where_count = 0
    result_orderby_field = ""
    result_order_direction = ""
    sql_aggregates = ""
    sql_wheres = ""
    sql_filters = ""

    if aggregates:
        aggregate_count = len(aggregates)
    if filters:
        where_count = len(filters)
    if orderby:
        result_orderby_field = orderby[0]
        result_order_direction = orderby[1]

    # aggregate list values
    if aggregates:
        for idx, aggregate in enumerate(aggregates):
            if (idx + 1) == aggregate_count:
                sql_aggregates = sql_aggregates + "{}".format(aggregate)
            else:
                sql_aggregates = sql_aggregates + "{}, ".format(aggregate)
    else:
        for idx, field in enumerate(fields):
            if (idx + 1) == field_count:
                sql_filters = sql_filters + "{} ".format(field)
            else:
                sql_filters = sql_filters + "{}, ".format(field)

    # where 'field' operator 'value'
    if filters:
        for idx, s_item in enumerate(filters):
            field = s_item[0]
            operator = s_item[1].upper()
            andor = ""
            if len(s_item) == 3:
                andor = s_item[2]
            if (idx + 1) == where_count:
                sql_wheres = sql_wheres + " {} {} ?".format(field, operator)
            else:
                if andor:
                    sql_wheres = sql_wheres + " {} {} ? {} ".format(field, operator, andor)
                else:
                    sql_wheres = sql_wheres + " {} {} ? ".format(field, operator)

    # all aggregated values where
    if sql_aggregates and sql_wheres:
        if result_orderby_field:
            result = "SELECT {} FROM {} WHERE {} ORDER BY {} {}}".format(sql_aggregates, name, sql_wheres,
                                                                         result_orderby_field, result_order_direction)
        else:
            result = "SELECT {} FROM {} WHERE {};".format(sql_aggregates, name, sql_wheres)
    # all aggregated values
    elif sql_aggregates and not sql_wheres:
        if result_orderby_field:
            result = "SELECT {} FROM {} ORDER BY {} {}".format(sql_aggregates, name, result_orderby_field,
                                                               result_order_direction)
        else:
            result = "SELECT {} FROM {};".format(sql_aggregates, name)
    # all everything where
    elif sql_wheres and not sql_aggregates:
        if result_orderby_field:
            result = "SELECT {} FROM {} WHERE {} ORDER BY {} {}".format(sql_filters, name, sql_wheres,
                                                                        result_orderby_field, result_order_direction)
        else:
            result = "SELECT {} FROM {} WHERE {};".format(sql_filters, name, sql_wheres)
    # all everything
    else:
        if result_orderby_field:
            result = "SELECT {} FROM {} ORDER BY {} {}".format(sql_filters, name, result_orderby_field,
                                                               result_order_direction)
        else:
            result = "SELECT {} FROM {};".format(sql_filters, name)
    return result.replace("  ", " ")
