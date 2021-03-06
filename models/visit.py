#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Visit module
"""

from models.query import Query
from util import utils

__module__ = "visit"


class Visit:
    """
    Visit class
    """

    def __init__(self):
        """
        Initialize current class
        """
        self.model = {
            "name": "visits",
            "id": "visit_id",
            "fields": ("visit_id", "report_id", "employee_id", "customer_id",
                       "visit_date", "po_sent",
                       "po_buyer", "po_number", "po_company", "po_address1", "po_address2",
                       "po_postcode", "po_postoffice", "po_country",
                       "po_note", "prod_demo", "prod_sale", "visit_type",
                       "po_sas", "po_sale", "po_total", "po_approved", "visit_note"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "INTEGER NOT NULL", "INTEGER NOT NULL", "INTEGER NOT NULL",
                      "TEXT NOT NULL", "INTEGER DEFAULT 0",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT", "TEXT NOT NULL",
                      "REAL DEFAULT 0", "REAL DEFAULT 0", "REAL DEFAULT 0",
                      "INTEGER DEFAULT 0", "TEXT")
        }
        self._visit = {}
        self._visits = []
        self._visits = []
        self._visits = []
        self._csv_record_length = 22
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def csv_record_length(self):
        """
        The number of fields expected on csv import
        """
        return self._csv_record_length

    @property
    def visit(self):
        """
        Visit
        Returns:
            The current active visit
        """
        return self._visit

    @property
    def visits(self):
        """
        Report Visit List
        Returns:
            The list of visits for a report_id
        """
        return self._visits

    def list_by_customer(self, customer_id):
        """
        Load the list of visits for a given customer
        Args:
            customer_id:
        """
        self.__get_by_customer(customer_id)

    def list_by_date(self, visit_date):
        """
        Load the list of visits for a given date
        Args:
             visit_date:
        """
        self.__get_by_date(visit_date)

    def list_by_report_id(self, report_id):
        """
        Load the list of visits for a given report
        Args:
            report_id:
        """
        self.__get_by_report_id(report_id)

    def load_visit(self, visit_id):
        """
        Load a visit
        Args:
            visit_id:
        """
        self.__get(visit_id)

    def add(self, report_id, employee_id, customer_id, workdate):
        """
        Create a new visit
        Args:
            report_id:
            employee_id:
            customer_id:
            workdate:
        Returns:
            integer:
        """
        values = (None, report_id, employee_id, customer_id, workdate, 0,
                  "", "", "", "", "", "", "", "", "", "", "", "", 0.0, 0.0, 0.0, 0, "")
        new_id = self.insert(values)
        self.__get(new_id)
        return new_id

    def clear(self):
        """
        Clear internal variables
        """
        self._visit = {}
        self._visits = []

    def delete(self, visit_id):
        """
        Delete the specified visit
        :param visit_id:
        :return:
        """
        filters = [(self.model["id"], "=")]
        values = (visit_id,)
        sql = self.q.build("delete", self.model, filters)
        self.q.execute(sql, values)

    def insert(self, values):
        """
        Insert a new row in the database
        :param values:
        :return: rownumber on success or None
        """
        sql = self.q.build("insert", self.model)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return None

    def recreate_table(self):
        """
        Recreate table
        """
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear()

    def translate_row_insert(self, row):
        """
        Translate a csv row
        :rtype: bool
        :param row:
        :return: True / False
        """
        # translate bool text to integer col 5
        field_5 = utils.bool2int(utils.arg2bool(row[5]))
        new_row = (row[0], row[1], row[2], row[3], row[4].strip(),
                   field_5, row[6].strip(), row[7].strip(), row[8].strip(), row[9].strip(),
                   row[10].strip(), row[11].strip(), row[12].strip(), row[13].strip(), row[14].strip(),
                   row[15].strip(), row[16].strip(), row[17].strip(), row[18], row[19],
                   row[20], row[21], row[14].strip())
        self.insert(new_row)  # call insert function

    def update(self):
        """
        Write visit changes to database
        :return: rownumber on success or None
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._visit.values())
        sql = self.q.build("update", self.model, update=fields, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return None

    def __get(self, visit_id):
        """
        Find the specified visit
        :param visit_id:
        :return: True on success
        """
        filters = [(self.model["id"], "=")]
        values = (visit_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._visit = dict(zip(self.model["fields"], data[0]))
                return True
            except IndexError:
                self._visit = {}
        return False

    def __get_by_customer(self, customer_id, visit_date=None):
        """
        Load visit_list_customer for specified customer
        :param customer_id:
        :param visit_date:
        """
        if visit_date:
            filters = [("customer_id", "=", "AND"), ("visit_date", "=")]
            values = (customer_id, visit_date)
        else:
            filters = [("customer_id", "=")]
            values = (customer_id,)

        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._visits = [dict(zip(self.model["fields"], row)) for row in data]
                self._visit = self._visits[0]
            except (IndexError, KeyError):
                self._visit = {}
                self._visits = []

    def __get_by_date(self, visit_date):
        """
        List visits by date
        :param visit_date:
        """
        filters = [("visit_date", "=")]
        values = (visit_date,)

        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._visits = dict(zip(self.model["fields"], data[0]))
                self._visit = self._visits[0]
            except IndexError:
                self._visit = {}
                self._visits = []

    def __get_by_report_id(self, report_id):
        """
        Load visit_list_customer for specified report
        :param: report_id
        """
        filters = [("report_id", "=")]
        values = (report_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._visits = [dict(zip(self.model["fields"], row)) for row in data]
                self._visit = self._visits[0]
            except (IndexError, KeyError):
                self._visit = {}
                self._visits = []
