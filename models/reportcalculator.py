# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Calculation module
"""

from models.query import Query


class ReportCalculator:
    """
    Calculator
    """

    def __init__(self):
        """
        Initialize Calculator
        """
        self.model = {
            "name": "reportcalculations",
            "id": "calc_id",
            "fields": ("calc_id", "calc_date", "report_id", "employee_id", "reports_calculated",
                       "new_visit", "new_demo", "new_sale", "new_turnover",
                       "recall_visit", "recall_demo", "recall_sale", "recall_turnover",
                       "sas", "sas_turnover", "current", "demo", "sale", "turnover",
                       "kmwork", "kmprivate", "workdays", "offdays"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT NOT NULL", "INTEGER NOT NULL", "INTEGER NOT NULL",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0",
                      "REAL DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "REAL DEFAULT 0",
                      "INTEGER DEFAULT 0", "REAL DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0",
                      "INTEGER DEFAULT 0", "REAL DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0")
        }
        self._totals = {}
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def item(self):
        """
        Totals
        Returns:
            The current current
        """
        return self._totals

    @item.setter
    def item(self, date_employee):
        """
        Sets the current totals
        :param date_employee: tuple with date and employee
        :return:
        """
        try:
            try:
                _ = self._totals["workdate"]
                if not _ == date_employee[0]:
                    self.get_by_date_employee(date_employee[0], date_employee[1])
            except KeyError:
                self.get_by_date_employee(date_employee[0], date_employee[1])
        except IndexError:
            self.clear()

    def clear(self):
        """
        Clear internal variables
        """
        self._totals = {}

    def get_by_id(self, calc_id):
        """
        Select by id
        Returns:
            bool indicating current has been set for the requested id
        """
        filters = [(self.model["id"], "=")]
        values = (calc_id,)

        sql = self.q.build("select", self.model, filters=filters)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            self._totals = dict(zip(self.model["fields"], data[0]))
        return False

    def get_by_date_employee(self, workdate, employee_id):
        """
        Select current for employeeid and workdate

        Args:
            workdate:
            employee_id:
        Returns:
            bool indicating current for the selected reportid is now set
        """
        filters = [("workdate", "=", "and"), ("employee_id", "=")]
        values = (workdate, employee_id)

        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            self._totals = dict(zip(self.model["fields"], data[0]))
        return False

    def insert(self, values):
        """
        Save values to database and sets current with the supplied values
        Args:
            values:
        """
        values = list(values)
        values[0:0] = [None]
        values = tuple(values)

        sql = self.q.build("insert", self.model)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            return data
        return False

    def update(self):
        """
        Update current in database if necessary

        Returns:
            bool indicating if update was a success
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._totals.values())

        sql = self.q.build("update", self.model, update=fields, filters=filters)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            return True
        return False

    def recreate_table(self):
        """
        Drop and init_detail table
        """
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear()
