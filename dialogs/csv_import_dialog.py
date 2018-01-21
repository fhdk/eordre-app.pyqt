#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox

from configuration import config
from resources.csv_import_dialog_rc import Ui_csvFileImportDialog
from util.worker import Worker

__module__ = "csv_import_dialog"


class CsvFileImportDialog(QDialog, Ui_csvFileImportDialog, QObject):
    """
    Dialog for importing CSV data
    """
    sig_done = pyqtSignal()

    def __init__(self, app, contacts, customers, employees, orderlines, reports, tables, visits):
        """Initialize Dialog"""
        super(CsvFileImportDialog, self).__init__()
        self.setupUi(self)
        self.__app = app
        self._contacts = contacts
        self._customers = customers
        self._orderlines = orderlines
        self._employees = employees
        self._reports = reports
        self._visits = visits

        self.file_dialog = QFileDialog()
        self.progressBar.setRange(0, 1)

        self.buttonImport.setEnabled(False)
        # connect to signals
        self.comboImport.currentIndexChanged.connect(self.combo_changed_action)
        self.buttonBrowse.clicked.connect(self.button_browse_action)
        self.buttonImport.clicked.connect(self.button_import_action)
        self.buttonClose.clicked.connect(self.button_close_action)
        self.txtSelectedFile.textChanged.connect(self.on_selected_file_changed)

        for item in tables:                                # Setup which tables can be imported
            self.comboImport.addItem(item[0], item[1])
            self.comboImport.setCurrentIndex(0)
        self.browseDir = config.HOME                       # setup file import dir to home
        self.selectedFile = ""                             # initalize selected file
        self.selectedTable = self.comboImport.itemData(0)  # initialize selected table

        self.__workers_done = 0
        self.__threads = []

    def button_browse_action(self):
        """Slot for buttonBrowse clicked signal"""
        # browse for import file
        data = self.file_dialog.getOpenFileName(self,
                                                "Vælg import fil",
                                                self.browseDir,
                                                "Text files (*.csv)")
        self.selectedFile = data[0]
        self.browseDir = os.path.dirname(data[0])
        self.txtSelectedFile.setText(self.selectedFile)

    def button_close_action(self):
        """Slot for buttonClose clicked signal"""
        if not self.__workers_done == 5:
            self.sig_done.emit()
        self.done(False)

    def button_import_action(self):
        """
        Slot for buttonImport clicked signal
        """
        self.buttonClose.setEnabled(False)
        headers = True
        if not self.checkHeaders.isChecked():
            headers = False
        self.progressBar.setRange(0, 0)  # set spinning progressbar

        if self.selectedFile:
            # import selected file to contact table
            if self.selectedTable == "contacts":
                worker = Worker(1, self.__app)
                thread = QThread(self)
                thread.setObjectName("contacts_csv")
                self.__threads.append((thread, worker))
                worker.moveToThread(thread)
                worker.sig_status.connect(self.on_status)
                worker.sig_done.connect(self.on_done)
                try:
                    thread.started.connect(
                        worker.import_contacts_csv(
                            self._contacts, self.selectedFile, header=headers))
                    thread.start()
                except TypeError:
                    pass

            # import selected file to customer table
            if self.selectedTable == "customers":
                worker = Worker(2, self.__app)
                thread = QThread(self)
                thread.setObjectName("customers_csv")
                self.__threads.append((thread, worker))
                worker.moveToThread(thread)
                worker.sig_status.connect(self.on_status)
                worker.sig_done.connect(self.on_done)
                try:
                    thread.started.connect(
                        worker.import_customers_csv(
                            self._customers, self.selectedFile, header=headers))
                    thread.start()
                except TypeError:
                    pass

            # import selected file to lines table
            if self.selectedTable == "lines":
                worker = Worker(4, self.__app)
                thread = QThread(self)
                thread.setObjectName("orderlines_csv")
                self.__threads.append((thread, worker))
                worker.moveToThread(thread)
                worker.sig_status.connect(self.on_status)
                worker.sig_done.connect(self.on_done)
                try:
                    thread.started.connect(
                        worker.import_orderlines_csv(
                            self._orderlines, self.selectedFile, header=headers))
                    thread.start()
                except TypeError:
                    pass

            # import selected file to report table
            if self.selectedTable == "reports":
                worker = Worker(5, self.__app)
                thread = QThread(self)
                thread.setObjectName("reports_csv")
                self.__threads.append((thread, worker))
                worker.moveToThread(thread)
                worker.sig_status.connect(self.on_status)
                worker.sig_done.connect(self.on_done)
                try:
                    thread.started.connect(
                        worker.import_reports_csv(
                            self._employees.employee["employee_id"], self._reports, self.selectedFile, header=headers))
                    thread.start()
                except TypeError:
                    pass

            # import selected file to visit table
            if self.selectedTable == "visits":
                worker = Worker(3, self.__app)
                thread = QThread(self)
                thread.setObjectName("visits_csv")
                self.__threads.append((thread, worker))
                worker.moveToThread(thread)
                worker.sig_status.connect(self.on_status)
                worker.sig_done.connect(self.on_done)
                try:
                    thread.started.connect(
                        worker.import_visits_csv(
                            self._visits, self.selectedFile, header=headers))
                    thread.start()
                except TypeError:
                    pass

            self.selectedFile = ""
            self.txtSelectedFile.clear()
            self.comboImport.removeItem(self.comboImport.currentIndex())
            self.comboImport.setCurrentIndex(0)

        self.buttonImport.setEnabled(False)  # disable the button until next file is selected
        self.buttonBrowse.setEnabled(True)   # enable browse button
        self.buttonClose.setEnabled(True)    # enable close button

    @pyqtSlot(name="combo_changed_action")
    def combo_changed_action(self):
        """Slot for ComboBox currentIndexChanged signal"""
        self.selectedTable = self.comboImport.itemData(self.comboImport.currentIndex())

    @pyqtSlot(int, name="on_done")
    def on_done(self, worker_id: int):
        """
        Executes when the import is done
        """
        self.__workers_done += 1
        if self.__workers_done == 5:
            self.sig_done.emit()
            self.button_close_action()
        self.progressBar.setRange(0, 1)
        self.buttonImport.setEnabled(False)  # disable the button till next file is selected
        self.buttonBrowse.setEnabled(True)   # enable browse button
        self.buttonClose.setEnabled(True)    # enable close button

    @pyqtSlot(int, str, name="on_status")
    def on_status(self, worker_id: int, text: str):
        """
        Process status notification
        """
        self.log.append(text)
        if text.startswith("ERROR") or text.startswith("FEJL"):
            title = "Import fejl"
            msg = QMessageBox()
            msg.information(self, title, "{}: {}".format(worker_id, text), QMessageBox.Ok)

    @pyqtSlot(name="on_selected_file_changed")
    def on_selected_file_changed(self):
        self.selectedFile = self.txtSelectedFile.text()
        if self.selectedFile.endswith(".csv"):
            self.buttonImport.setEnabled(True)
        else:
            self.buttonImport.setEnabled(False)
