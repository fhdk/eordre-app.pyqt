#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Employee Module
"""

from models.query import Query
from models.settings import Settings
from util import httpFn, rules

__module__ = "employee"


class Employee:
    """
    Employee class
    """

    def __init__(self):
        """
        Initialize Employee class
        """
        self.model = {
            "name": "employees",
            "id": "employee_id",
            "fields": ("employee_id", "salesrep", "fullname", "email", "country", "sas"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER DEFAULT 0")
        }
        self._employee = {}
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)
        self.s = Settings()
        if rules.check_settings(self.s.settings):
            self.load(self.s.settings["usermail"])

    @property
    def employee(self):
        """
        Return current and only employeeid
        """
        return self._employee

    def insert(self, values):
        """
        Insert employee in database
        Args:
            values:
        """
        sql = self.q.build("insert", self.model)
        self.q.execute(sql, values=values)

    def load(self, email):
        """
        Load the employee
        """
        filters = [("email", "=")]
        values = (email,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values)
        # first check if employee is loaded
        # second check is in exception handling
        try:
            _ = data[0]
            self._employee = dict(zip(self.model["fields"], data[0]))
        except IndexError:
            if httpFn.inet_conn_check():
                # load from http
                self.load_from_http()
                success, data = self.q.execute(sql, values)
                try:
                    # second check after load_from_http
                    _ = data[0]
                    self._employee = dict(zip(self.model["fields"], data[0]))
                except IndexError:
                    self._employee = {}

    def load_from_http(self):
        """
        Load employee from http
        """
        self.s.get()
        data = httpFn.get_employee_data(self.s)
        if data:
            data = list(data)
            data[0:0] = [None]
            self.insert(tuple(data))

    def update(self):
        """
        Update employee in database
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._employee.values())

        sql = self.q.build("update", self.model, update=fields, filters=filters)

        self.q.execute(sql, values=values)
