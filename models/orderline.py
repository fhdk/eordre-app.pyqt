#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Visit details module
"""

from models.query import Query
from util import utils, printFn as p

__module__ = "orderline"


class OrderLine:
    """
    OrderLine class
    """

    def __init__(self):
        """
        Initialize OrderLine class
        """
        self.model = {
            "name": "orderlines",
            "id": "line_id",
            "fields": ("line_id", "visit_id",
                       "pcs", "sku", "text", "price", "sas", "discount",
                       "linetype", "linenote", "item"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "INTEGER NOT NULL",
                      "INTEGER", "TEXT", "TEXT", "REAL", "INTEGER DEFAULT 0", "REAL DEFAULT 0",
                      "TEXT", "TEXT", "TEXT")
        }
        self._line = {}
        self._lines = []
        self._csv_record_length = 8
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def line(self):
        """
        Return the current focused purchase order line
        Returns:
             current
        """
        return self._line

    @line.setter
    def line(self, line_id):
        """
        Set the current focused purchase order line
        Args:
            line_id:
        """
        try:
            _ = self._line["line_id"]
            if not _ == line_id:
                self.find(line_id=line_id)
        except KeyError:
            self.find(line_id=line_id)

    @property
    def list_(self):
        """
        All purchase order lines
        Returns:
            List of details for a purchase order line
        """
        return self._lines

    @list_.setter
    def list_(self, visit_id):
        """
        Orderlines setter. Load purchase order lines for visit_id
        Args:
            visit_id:
        """
        try:
            v_id = self._lines[0]
            if not v_id == visit_id:
                self.load_visit(visit_id=visit_id)
        except (IndexError, KeyError):
            self.load_visit(visit_id)

    @property
    def csv_record_length(self):
        """The number of fields expected on csv import"""
        return self._csv_record_length

    def add(self, visit_id, line_type):
        """
        Initialize a new purchase order line with visitid
        Args:
            visit_id:
            line_type:
        """
        line_type = line_type.upper()
        values = (None, visit_id, "", "", "", "", "", "", line_type, "", "")
        new_id = self.insert(values)
        self.find(new_id)

    def clear(self):
        """
        Clear internal variables
        """
        self._line = {}
        self._lines = []

    def delete(self, orderline_id):
        """
        Delete line with id
        Args:
            orderline_id:
        Returns:
            bool
        """
        filters = [(self.model["id"], "=")]
        values = (orderline_id,)
        sql = self.q.build("delete", self.model, filters=filters)
        success, data = self.q.execute(sql, values)
        if success and data:
            return True
        return False

    def find(self, line_id):
        """
        Find the the order line with id
        Args:
            line_id:
        Returns:
            bool
        """
        filters = [(self.model["id"], "=")]
        values = (line_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._line = dict(zip(self.model["fields"], data[0]))
                return True
            except IndexError:
                self._line = {}
        return False

    def import_csv(self, row):
        """
        Translate a csv row
        Args:
            row:
        """
        # translate bool text to integer col 6
        field_6 = utils.bool2int(utils.arg2bool(row[6]))
        new_row = (row[0], row[1], row[2], row[3].strip(), row[4].strip(), row[5], field_6, row[7], "S", "", "")
        self.insert(new_row)

    def insert(self, values):
        """
        Insert a new line with values
        Args:
            values:
        Returns:
            rownumber or None
        """
        sql = self.q.build("insert", self.model)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return None

    def load_visit(self, visit_id):
        """
        Load order lines for visit_id
        Args:
            visit_id:
        Returns:
            bool: True on success
        """
        filters = [("visit_id", "=")]
        values = (visit_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._lines = [dict(zip(self.model["fields"], row)) for row in data]
                self._line = self.list_[0]
                return True
            except (IndexError, KeyError):
                self._line = {}
                self._lines = []
        return False

    def recreate_table(self):
        """
        Recrete table and clears internal variables
        """
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear()

    def save_all(self):
        """
        Save the list of lines
        """
        for line in self._lines:
            if line[self.model["id"]] is None:
                self.insert(line.values())
            else:
                self._line = line
                self.update()

    def update(self):
        """
        Update line data in database
        Returns:
            rownumber or None
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._line.values())
        sql = self.q.build("update", self.model, update=fields, filters=filters)
        if sql.startswith("ERROR"):
            return None
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return None
