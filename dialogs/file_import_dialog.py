#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <f@hundewadt.dk>
# Copyright: Frede Hundewadt <fh@uex.dk>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QDialog, QFileDialog

from configuration import config
from models import contact, customer, visit, orderline, report
from resources import file_import_dialog_rc


class Communication(QObject):
    customersdone = pyqtSignal()


class FileImportDialog(QDialog, file_import_dialog_rc.Ui_FileImportDialog):
    def __init__(self, table_list, parent=None):
        """Initialize Dialog"""
        super(FileImportDialog, self).__init__(parent)
        self.file_dialog = QFileDialog()  # Create FileDialog object
        self.c = Communication()
        self.setupUi(self)

        self.buttonImport.enabled = False
        # connect to signals
        self.comboImport.currentIndexChanged.connect(self.combo_current_index_changed_action)
        self.buttonBrowse.clicked.connect(self.button_browse_action)
        self.buttonImport.clicked.connect(self.button_import_action)
        self.buttonClose.clicked.connect(self.button_close_action)
        # Setup which tables can be imported
        for table_item in table_list:
            self.comboImport.addItem(table_item[0], table_item[1])
            self.comboImport.setCurrentIndex(0)
        self.browseDir = config.HOME  # setup file import dir to home
        self.selectedFile = ""  # initalize selected file
        self.selectedTable = self.comboImport.itemData(0)  # initialize selected table
        # initialize objects
        self.Contact = contact.Contact()  # Create Contact object
        self.Customer = customer.Customer()  # Create Customer object
        self.OrderVisit = visit.Visit()  # Create OrderVisit object
        self.OrderLine = orderline.OrderLine()  # Create OrderLine object
        self.Report = report.Report()  # Create Report object

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
        self.done(False)

    def button_import_action(self):
        """Slot for buttonImport clicked signal"""
        # we dont want buttons to be activated twice during import
        self.buttonImport.enabled = False
        self.buttonBrowse.enabled = False
        self.buttonClose.enabled = False

        if self.selectedFile:
            # notice to add to list box
            notice = self.comboImport.currentText() + " er importeret."

            # import selected file to contact table
            if self.selectedTable == "contact":
                self.Contact.import_csv(self.selectedFile, self.checkHeaders.isChecked())
                self.listImported.addItem(notice)
                self.c.customersdone.emit()

            # import selected file to customer table
            if self.selectedTable == "customer":
                self.Customer.import_csv(self.selectedFile, self.checkHeaders.isChecked())
                self.listImported.addItem(notice)

            # import selected file to ordervisit table
            if self.selectedTable == "visit":
                self.OrderVisit.import_csv(self.selectedFile, self.checkHeaders.isChecked())
                self.listImported.addItem(notice)

            # import selected file to orderline table
            if self.selectedTable == "orderline":
                self.OrderLine.csv_import(self.selectedFile, self.checkHeaders.isChecked())
                self.listImported.addItem(notice)

            # import selected file to report table
            if self.selectedTable == "report":
                self.Report.import_csv(self.selectedFile, self.checkHeaders.isChecked())
                self.listImported.addItem(notice)

            self.selectedFile = ""
            self.txtSelectedFile.setText(self.selectedFile)
            self.comboImport.removeItem(self.comboImport.currentIndex())
            self.comboImport.setCurrentIndex(0)

        self.buttonImport.enabled = False  # disable the button till next file is selected
        self.buttonBrowse.enabled = True  # enable browse button
        self.buttonClose.enabled = True  # enable close button

    def combo_current_index_changed_action(self):
        """Slot for ComboBox currentIndexChanged signal"""
        self.selectedTable = self.comboImport.itemData(self.comboImport.currentIndex())