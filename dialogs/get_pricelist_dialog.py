#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from PyQt5.QtCore import QThread, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QDialog

from util.worker import Worker
from resources.http_products_dialog_rc import Ui_getProductsHttpDialog

B_COLOR = "\033[0;37m"
E_COLOR = "\033[0;m"
DBG = True

__module__ = "products_http"


def printit(string):
    """Print a variable string for debug purposes"""
    print("{}\n{}{}{}".format(__module__, B_COLOR, string, E_COLOR))


class GetPricelistDialog(QDialog, Ui_getProductsHttpDialog):
    """
    Dialog for importing products from server
    """
    sig_done = pyqtSignal()

    def __init__(self, app, products, settings, parent=None):
        """
        Initialize Dialog
        Args:
            products: main product object
            settings: main current object
        """
        super(GetPricelistDialog, self).__init__(parent)
        self.setupUi(self)
        self.__app = app
        self.products = products
        self.settings = settings
        # connect signals
        self.buttonStart.clicked.connect(self.button_start_action)
        self.buttonClose.clicked.connect(self.button_close_action)

        self.__workers_done = 0
        self.__threads = []

    @pyqtSlot()
    def button_close_action(self):
        """Slot for buttonClose clicked signal"""
        self.done(True)

    @pyqtSlot()
    def button_start_action(self):
        """Slot for buttonStart clicked signal"""
        self.progressBar.setRange(0, 0)
        self.buttonStart.setEnabled(False)
        self.buttonClose.setEnabled(False)
        worker = Worker(20, self.__app)
        thread = QThread(self)
        thread.setObjectName("products_http")
        self.__threads.append((thread, worker))
        worker.moveToThread(thread)
        worker.sig_status.connect(self.on_status)
        worker.sig_done.connect(self.on_done)
        try:
            thread.started.connect(worker.import_products_http(self.products, self.settings))
            thread.start()
        except TypeError as t:
            if DBG:
                printit(" ->products -> http\n ->exception handled: {}".format(t))

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
