#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Report class"""

from datetime import datetime
from operator import itemgetter

from models.reportcalculator import ReportCalculator
from models.query import Query
from util import utils

__module__ = "report"


class Report:
    """
    Report
    """

    def __init__(self):
        """
        Initilize Report class
        """
        self.model = {
            "name": "reports",
            "id": "report_id",
            "fields": ("report_id", "employee_id", "rep_no", "rep_date", "timestamp",
                       "newvisitday", "newdemoday", "newsaleday", "newturnoverday",
                       "recallvisitday", "recalldemoday", "recallsaleday", "recallturnoverday",
                       "sasday", "sasturnoverday", "demoday", "saleday",
                       "kmmorning", "kmevening", "supervisor", "territory",
                       "workday", "infotext", "sent", "offday", "offtext", "kmprivate"),
            "types": ("INTEGER PRIMARY KEY NOT NULL",
                      "INTEGER NOT NULL", "INTEGER NOT NULL", "TEXT NOT NULL", "TEXT NOT NULL",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "REAL DEFAULT 0",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "REAL DEFAULT 0",
                      "INTEGER DEFAULT 0", "REAL DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "TEXT", "TEXT",
                      "INTEGER DEFAULT 0", "TEXT", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "TEXT",
                      "INTEGER DEFAULT 0")
        }
        self._reports = []
        self._report = {}
        self._csv_record_length = 25
        self.q = Query()
        self.c = ReportCalculator()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def csv_record_length(self):
        """The number of fields expected on csv import"""
        return self._csv_record_length

    @property
    def report(self):
        """
        Report
        Returns:
            Active report
        """
        return self._report

    @property
    def reports(self):
        """
        Report List
        Returns:
            Current list of reports
        """
        try:
            _ = self._reports[0]
        except (IndexError, KeyError):
            self.__get_by_period()
        return self._reports

    def clear(self):
        """
        Clear internal variables
        """
        self.c.clear()
        self._report = {}
        self._reports = []

    def create(self, employee, workdate):
        """
        Create reportid for employeeid and date supplied
        Args:
            :type employee: object
            :type workdate: str iso formatted representing the work date
        """
        # we need to find the number of reports for the month of the supplied date
        # then init_detail 1 to that number
        # we need to calculate the sums for the previous reportid for month
        # those sums will be stored in seperate table
        # creating a new table with
        #           sum demoes & sum sales
        # |  *  |              DAY               |             MONTH              |
        # | --- | ------------------------------ | ------------------------------ |
        # |  *  | Visit | Demo | Sale | Turnover | Visit | Demo | Sale | Turnover |
        # | --- | ------------------------------ | ------------------------------ |
        # |  N  |  sum     sum   sum      sum       sum     sum    sum    sum
        # |  R  |  sum     sum   sum      sum       sum     sum    sum    sum
        # | SAS |                sum      sum                      sum    sum
        # | SUM |  sum     sum   sum      sum       sum     sum    sum    sum

        # parameters for initial feed of ReportCalc
        # aggregates
        aggregates = ["count(report_id) AS 'report_count'",
                      "sum(newvisitday) AS 'new_visit'",
                      "sum(newdemoday) AS 'new_demo'",
                      "sum(newsaleday) AS 'new_sale'",
                      "sum(newturnoverday) AS 'new_turnover'",
                      "sum(recallvisitday) AS 'recall_visit'",
                      "sum(recalldemoday) AS 'recall_demo'",
                      "sum(recallsaleday) AS 'recall_sale'",
                      "sum(recallturnoverday) AS 'recall_turnover'",
                      "sum(sasday) AS 'sas'",
                      "sum(sasturnoverday) AS 'sas_turnover'",
                      "(sum(newvisitday) + sum(recallvisitday)) AS 'current'",
                      "(sum(newdemoday) + sum(recalldemoday)) AS 'demo'",
                      "(sum(newsaleday) +  sum(recallsaleday) + sum(sasday)) AS 'sale'",
                      "(sum(newturnoverday) + sum(recallturnoverday) + sum(sasturnoverday)) AS 'turnover'",
                      "(sum(kmevening - kmmorning)) AS 'kmwork'",
                      "(sum(kmprivate)) AS 'kmprivate'",
                      "(sum(workday = 1)) AS 'workdays'",
                      "(sum(offday = 1)) AS 'offdays'"]
        filters = [("rep_date", "LIKE", "and"), ("employee_id", "=", "and"), ("sent", "=")]
        ym_filter = "{}%".format(workdate[:8])
        employee_id = employee["employee_id"]
        territory = employee["salesrep"]
        values = (ym_filter, employee_id, 1)

        sql = self.q.build("select", self.model, aggregates=aggregates, filters=filters)

        success, data = self.q.execute(sql, values)

        if success and data:
            # assign expected result from list item
            try:
                _ = data[0]
            except IndexError:
                return False
            # temporary convert tuple to list
            current_month_totals = list(data[0])
            # extract report count from first column
            report_count = int(current_month_totals[0])
            # increment report count
            next_report = report_count + 1
            # init_detail a combined list with the identifiers and the totals
            current_month_totals = [workdate, "None", employee_id] + current_month_totals
            timestamp = datetime.today()
            # init_detail tuple with values to initialze the new report
            new_report_values = (None, employee_id, next_report, workdate, timestamp,
                                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                 0, 0, "", territory, 1, "", 0, 0, "", 0)
            # assign return value as new report_id
            report_id = self.insert(new_report_values)
            # insert report_id to identify for which report the totals was calculated
            current_month_totals[1] = report_id
            # revert to tuple
            current_month_totals = tuple(current_month_totals)
            # insert the values in the calculation table
            self.c.insert(current_month_totals)
            return True
        else:
            return False

    def insert(self, values):
        """
        Insert new reportid in table
        Args:
            :type values: iterable
        """
        sql = self.q.build("insert", self.model)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            return data
        return False

    def load(self, workdate=None, year=None, month=None):
        """
        Load reports for a given period
        If none given load all
        Args:
            :type workdate: str
            :type year: str
            :type month: str
        """
        self.__get_by_period(workdate, year, month)

    def recreate_table(self):
        """
        Drop and initialize reports table
        """
        self.c.recreate_table()
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear()

    def translate_row_insert(self, row, employee_id):
        """
        Translate a csv row
        Args:
            :type row: iterable
            :type employee_id: int
        """
        # translate bool text to integer for col 19, 21
        field_19 = utils.bool2int(utils.arg2bool(row[19]))
        field_21 = utils.bool2int(utils.arg2bool(row[21]))
        # create timestamp
        local_timestamp = datetime.today()
        values = (row[0], employee_id, row[1], row[2].strip(), local_timestamp, row[3],
                  row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12],
                  row[13], row[14], row[15], row[16], row[17].strip(), row[18].strip(),
                  field_19, row[20].strip(), field_21, row[22], row[23].strip(), row[24])

        self.insert(values)

    def update(self):
        """
        Update reportid in database
        """
        # update_list = list(self.model["fields"])[1:]
        # update_where = [(self.model["id"], "=")]
        # self.q.values_to_update(self._report.values())

        # if DBG:
        #     printit(
        #         "{}\n ->update\n  ->sql: {}\n  ->values: {}".format(
        #             sql, values))

        # if DBG:
        #     printit(
        #         "{}\n ->update\n  ->success: {}\n  ->data: {}".format(
        #             success, data))
        pass

    def __get_by_period(self, workdate=None, year=None, month=None):
        """
        Load reports matching args or all if no args
        Args:
            :type workdate: str
            :type year: str
            :type month: str
        """
        if workdate:
            try:
                _ = self._reports[0]
                for report in self._reports:
                    if report["workdate"] == workdate:
                        self._report = report
                        return
            except (IndexError, KeyError):
                pass

        filters = [("rep_date", "like")]
        value = "{}-{}-{}".format("%", "%", "%")
        if year:
            value = "{}-{}-{}".format(year, "%", "%")
        if year and month:
            value = "{}-{}-{}".format(year, month, "%")

        values = (value,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            try:
                _ = data[0]
                self._reports = [dict(zip(self.model["fields"], row)) for row in data]
                self._reports = sorted(self._reports, key=itemgetter("rep_date"), reverse=True)
                if workdate:
                    for report in self._reports:
                        if report["rep_date"] == workdate:
                            self._report = report
                            break
                if not self._report:
                    self._report = self._reports[0]
            except IndexError:
                self._report = {}
                self._reports = []
        else:
            self._report = {}
            self._reports = []
