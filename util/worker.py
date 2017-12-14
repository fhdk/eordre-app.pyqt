#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# code from https://stackoverflow.com/a/41605909
#
"""Worker module"""

import csv

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from util import httpFn

__module__ = "worker"


class Worker(QObject):
    """
    Must derive from QObject in order to emit signals, connect slots to other signals, and operate in a QThread.
    """

    sig_status = pyqtSignal(int, str)  # worker id, progress: emitted every step through the file
    sig_done = pyqtSignal(int)  # worker id: emitted at end of the file

    def __init__(self, thread_id: int, app):
        super().__init__()
        self.__app = app
        self.__thread_id = thread_id
        self.__abort = False

    @pyqtSlot(name="import_contacts_csv")
    def import_contacts_csv(self, contacts, filename, header):
        """
        Import contacts using csv file
        :param contacts: object
        :param filename: str
        :param header: bool
        :return:
        """
        filename.encode("utf8")
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder indlæsning ..."))
        contacts.recreate_table()
        ftext = ">>> Import er færdig!"
        with open(filename) as csvdata:
            reader = csv.reader(csvdata, delimiter="|")
            line = 0
            for row in reader:

                self.__app.processEvents()

                if not len(row) == contacts.csv_record_length:
                    ftext = "FEJL: Formatet i den valgte fil er ikke korrekt!"
                    break

                if header and line == 0:
                    line += 1
                    continue

                self.sig_status.emit(self.__thread_id, "{} - {}".format(row[2].strip(), row[3].strip()))

                contacts.translate_row_insert(row)  # send row to database

        self.sig_status.emit(self.__thread_id, "{}".format(ftext))
        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_customers_csv")
    def import_customers_csv(self, customers, filename, header):
        """
        Import customers using csv file
        :param customers:
        :param filename:
        :param header:
        :return:
        """
        filename.encode("utf8")
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder indlæsning ..."))
        customers.recreate_table()
        ftext = ">>> Import er færdig!"
        with open(filename) as csvdata:
            reader = csv.reader(csvdata, delimiter="|")
            rows = list(reader)
            for line, row in enumerate(rows):

                self.__app.processEvents()

                if not len(row) == customers.csv_record_length:
                    ftext = "FEJL: Formatet i den valgte fil er ikke korrekt!"
                    break

                if header and line == 0:
                    continue

                self.sig_status.emit(self.__thread_id, "{} - {}".format(row[1].strip(), row[2].strip()))

                customers.translate_row_insert(row)  # send row to database

        self.sig_status.emit(self.__thread_id, "{}".format(ftext))
        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_customers_http")
    def import_customers_http(self, customers, employees, settings):
        """
        Import customers using http
        :param customers:
        :param employees:
        :param settings:
        :return:
        """
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder hentning ..."))
        self.sig_status.emit(self.__thread_id, "{}".format("Henter fra server ..."))

        data = httpFn.get_customers(settings, employees)     # fetch datafile from http server
        for row in data:                                     # data processing

            self.__app.processEvents()

            self.sig_status.emit(self.__thread_id, "{} - {}".format(row[0], row[1]))

            customers.import_http(row)                       # init_detail row to database

        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_order_lines_csv")
    def import_orderlines_csv(self, orderlines, filename, header):
        """
        Import lines using csv file
        :param orderlines: OrderLine() class
        :param filename: filename to read
        :param header: bool if first line is header
        :return:
        """
        filename.encode("utf8")
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder indlæsning ..."))
        orderlines.recreate_table()
        ftext = ">>> Import er færdig!"
        with open(filename) as csvdata:
            reader = csv.reader(csvdata, delimiter="|")
            rows = list(reader)
            for line, row in enumerate(rows):

                self.__app.processEvents()

                if not len(row) == orderlines.csv_record_length:
                    ftext = "FEJL: Formatet i den valgte fil er ikke korrekt!"
                    break

                if header and line == 0:
                    continue

                self.sig_status.emit(self.__thread_id, "{} - {}".format(row[2].strip(), row[3].strip()))

                orderlines.translate_row_insert(row)              # send row to database

        self.sig_status.emit(self.__thread_id, "{}".format(ftext))
        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_products_http")
    def import_products_http(self, products, settings):
        """
        Import products using http
        :param products:
        :param settings:
        """
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder hentning ..."))
        products.drop_table()                               # drop product table
        self.sig_status.emit(self.__thread_id, "{}".format("Henter fra server ..."))
        data = httpFn.get_products(settings)                # fetching datafile using http with settings
        for row in data:                                    # process the data

            self.__app.processEvents()

            self.sig_status.emit(self.__thread_id, "{} - {}".format(row[0], row[1]))

            products.insert(row)                            # send row to database

        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_reports_csv")
    def import_reports_csv(self, employeeid, reports, filename, header):
        """
        Import reports using csv file
        :param employeeid
        :param reports:
        :param filename:
        :param header:
        :return:
        """
        filename.encode("utf8")
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder indlæsning ..."))
        reports.recreate_table()
        ftext = ">>> Import er færdig!"
        with open(filename) as csvdata:
            reader = csv.reader(csvdata, delimiter="|")
            rows = list(reader)

            for line, row in enumerate(rows):

                self.__app.processEvents()

                if not len(row) == reports.csv_record_length:
                    ftext = "FEJL: Formatet i den valgte fil er ikke korrekt!"
                    break

                if header and line == 0:
                    continue

                self.sig_status.emit(self.__thread_id, "{} - {}".format(row[2].strip(), row[3].strip()))

                reports.translate_row_insert(row, employeeid)  # send row to database

        self.sig_status.emit(self.__thread_id, "{}".format(ftext))
        self.sig_done.emit(self.__thread_id)

    @pyqtSlot(name="import_visits_csv")
    def import_visits_csv(self, visits, filename, header):
        """
        Import visits using csv file
        :param visits:
        :param filename:
        :param header:
        :return:
        """
        filename.encode("utf8")
        self.sig_status.emit(self.__thread_id, "{}".format("Forbereder indlæsning ..."))
        visits.recreate_table()
        ftext = ">>> Import er færdig!"
        with open(filename) as csvdata:
            reader = csv.reader(csvdata, delimiter="|")
            rows = list(reader)
            for line, row in enumerate(rows):

                self.__app.processEvents()

                if not len(row) == visits.csv_record_length:
                    ftext = "FEJL: Formatet i den valgte fil er ikke korrekt!"
                    break

                if header and line == 0:
                    continue

                self.sig_status.emit(self.__thread_id, "{} - {}".format(row[2].strip(), row[3].strip()))

                visits.translate_row_insert(row)                  # send row to database

        self.sig_status.emit(self.__thread_id, "{}".format(ftext))
        self.sig_done.emit(self.__thread_id)
