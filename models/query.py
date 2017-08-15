#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <f@hundewadt.dk>
# Copyright: Frede Hundewadt <fh@uex.dk>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Sqlite Query Module"""

import sqlite3

from configuration import config
from models.builders.build_create_query import build_create_query
from models.builders.build_delete_query import build_delete_query
from models.builders.build_drop_query import build_drop_query
from models.builders.build_insert_query import build_insert_query
from models.builders.build_select_query import build_select_query
from models.builders.build_update_query import build_update_query

B_COLOR = "\033[0;36m"
E_COLOR = "\033[0;m"
DBG = False

__module__ = "query"


def printit(string):
    """Print a variable string for debug purposes"""
    print("{}\n{}{}{}".format(__module__, B_COLOR, string, E_COLOR))


class Query:
    """
    Query Build and Execute
    """

    def build(self, query_type, model_def, selection=None, update=None, aggregates=None, filters=None, orderby=None):
        """
        Builds a sql query from definition

        Args:
            query_type: create(table), drop(table), insert(row), select(row), update(row), delete(row))

            model_def: table model definition
            {"name": ("name" ...), "fields": ("field" ...), "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT" ...)}

            selection: limit the result to selection

            update: fields to update
            ("field", "field" ...)

            aggregates: valid ["sum(column) AS 'expression'", "sum(column) AS 'expression'" ....]

            filters:  valid for all-, required for update- and delete query
            [("field", "operator", "value", "and/or"), (("field", "operator", "value"))]]

            orderby: asc or desc

        Returns:
            string with sql query

        """

        querytype = query_type.upper()
        if querytype not in ["CREATE", "DELETE", "DROP", "INSERT", "SELECT", "UPDATE"]:
            return "ERROR! Unsupported type: {}, {}".format(querytype, model_def["name"])

        if querytype == ["DELETE"]:
            if not filters:
                return "ERROR! Missing 'filters' for: {}, {}".format(querytype, model_def["name"])

        if querytype == ["UPDATE"]:
            if not filters or not update:
                return "ERROR! Missing 'update' or 'filters' for: {}, {}".format(querytype, model_def["name"])

        if orderby:
            orderby = orderby[1].upper()
            if not orderby == "ASC" or not orderby == "DESC":
                orderby = None

        # build init_detail table query
        if querytype == "CREATE":
            return build_create_query(model_def)

        # build delete row query
        if querytype == "DELETE":
            return build_delete_query(model_def, filters)

        # builds drop table query
        if querytype == "DROP":
            return build_drop_query(model_def)

        # build insert row query
        if querytype == "INSERT":
            return build_insert_query(model_def)

        # build all row query
        if querytype == "SELECT":
            return build_select_query(model_def, selection, aggregates, filters, orderby)

        # build update row query
        if querytype == "UPDATE":
            return build_update_query(model_def, update, filters)

    def execute(self, sql_query, values=None):
        """
        Execute a query and return the result
        Args:
            sql_query:
            values:
        Returns:
            list with result of the query - may be an empty list
        """
        if config.DEBUG_QUERY:
            printit(" ->execute\n"
                    "  ->sql: {}\n"
                    "  ->values: {}".format(sql_query, values))
        # query types: create, drop, delete, insert, select, update
        # specifically the select and insert query has to return the result
        select = sql_query.startswith("SELECT")  # returns data
        insert = sql_query.startswith("INSERT")  # returns rowid for the last inserted record
        db = sqlite3.connect(config.DBPATH)
        with db:
            try:
                result = None
                cur = db.cursor()
                if values:
                    cur.execute(sql_query, values)
                else:
                    cur.execute(sql_query)
                db.commit()
                if select:
                    result = cur.fetchall()
                if insert:
                    result = cur.lastrowid
            except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
                if config.DEBUG_QUERY:
                    printit("  ->exception: {}".format(e))
                return False, e
        if config.DEBUG_QUERY:
            printit("  ->result: {}\r".format(result))
        return True, result

    @staticmethod
    def values_to_arg(values):
        """
        Moves the id field from first to last element
        Args:
            values:

        Returns:
            Value list with id as the last field
        """
        work = list(values)
        rowid = work[0]
        work = work[1:]
        work.append(rowid)
        work = tuple(work)
        return work

    def exist_table(self, table):
        """
        Check database if tablename exist
        Args:
            table:

        Returns:
             bool indicating if table was found
        """
        statement = "SELECT name FROM sqlite_master WHERE type='{}' AND name='{}';".format("table", table)

        success, data = self.execute(statement)
        if data:
            return True
        return False
