#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog

from util.worker import Worker
from resources.http_customers_dialog_rc import Ui_getCustomersHttpDialog

B_COLOR = "\033[0;37m"
E_COLOR = "\033[0;m"
DBG = False

__module__ = "get_customers_dialog.py"


def printit(string):
    """Print a variable string for debug purposes"""
    print("{}\n{}{}{}".format(__module__, B_COLOR, string, E_COLOR))


class GetCustomersDialog(QDialog, Ui_getCustomersHttpDialog):
    """
    Import customers from http
    """

    sig_done = pyqtSignal()

    def __init__(self, app, customers, employees, settings):
        """
        Initialize Dialog
        Args:
            customers: main current object
            employees: main employeeid object
            settings: main current object
        """
        super(GetCustomersDialog, self).__init__()
        self.setupUi(self)
        self.__app = app
        self.customers = customers
        self.employees = employees
        self.settings = settings

        # connect signals
        self.buttonStart.clicked.connect(self.button_start_action)
        self.buttonClose.clicked.connect(self.button_close_action)

        self.__workers_done = 0
        self.__threads = []

    def button_close_action(self):
        """Slot for buttonClose clicked signal"""
        self.done(True)

    def button_start_action(self):
        """Slot for buttonStart clicked signal"""
        self.progressBar.setRange(0, 0)
        worker = Worker(10, self.__app)
        thread = QThread(self)
        thread.setObjectName("customers_http")
        self.__threads.append((thread, worker))
        worker.moveToThread(thread)
        worker.sig_status.connect(self.on_status)
        worker.sig_done.connect(self.on_done)
        try:
            """
            customers object is used by the worker to insert data into customer table
            employees object is used to fetch the customer file
            settings object is used to check access
            """
            thread.started.connect(worker.import_customers_http(self.customers, self.employees, self.settings))
            thread.start()
        except TypeError as t:
            if DBG:
                printit(" ->customers -> http\n ->exception handled: {}".format(t))

    @pyqtSlot()
    def on_done(self):
        """Slot for import thread finished signal"""
        self.buttonStart.setEnabled(True)
        self.buttonClose.setEnabled(True)
        self.progressBar.setRange(0, 1)
        self.sig_done.emit()
        self.button_close_action()

    @pyqtSlot(int, str)
    def on_status(self, worker_id: int, text: str):
        """Slot for import thread processing signal"""
        # status = "{}-{}".format(worker_id, text)
        self.log.append(text)
