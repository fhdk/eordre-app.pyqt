#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Visit Dialog Module
"""
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QTableWidgetItem

from models.orderline import OrderLine
from resources.visit_dialog_rc import Ui_visitDialog
from util import utils, printFn as p

__module__ = "visit_dialog.py"


class VisitDialog(QDialog, Ui_visitDialog):
    """
    Dialog for creating a new current
    """

    def __init__(self, customers, employees, products, reports, visits, parent=None):
        """
        Initialize
        Args:
            customers:
            employees:
            products:
            reports:
            visits:
            parent:
        """
        super(VisitDialog, self).__init__(parent)
        self.setupUi(self)
        self._customerid = customers.customer["customer_id"]
        self._employeeid = employees.employee["employee_id"]
        self._reportid = reports.report["report_id"]
        self._workdate = reports.report["rep_date"]
        self._products = products.list_
        self.txtVisitDate.setText(self._workdate)

        # p.debug("{} {}".format(__module__, "init"), "products", self._products)
        # exit(p.DEBUG)

        self._visits = visits
        self._visits.clear()
        try:
            """
            load visits for workdate
            """
            self._visits.load_for_customer(self._customerid, self._workdate)
            _ = self._visits.visit["visit_id"]

        except KeyError:
            self._visits.add(self._reportid, self._employeeid, self._customerid, self._workdate)
            self._visits.visit["visit_type"] = "R"
            if customers.customer["account"] == "NY":
                self._visits.customer["visit_type"] = "N"

        self._orderlines = OrderLine()
        self._orderlines.load_visit(self._visits.visit["visit_id"])
        for idx, detail in enumerate(self._orderlines.list_):
            # "pcs", "sku", "text", "price", "sas", "discount", "linetype", "extra"
            row_count = idx + 1
            self.widgetVisitDetails.setRowCount(row_count)
            self.widgetVisitDetails.setRowHeight(row_count, 20)
            w = QTableWidgetItem()
            w.setText(detail["linetype"])
            self.widgetVisitDetails.setItem(row_count, 0, w)
            w.setText(str(detail["pcs"]))
            self.widgetVisitDetails.setItem(row_count, 1, w)
            w.setText(detail["item"])
            self.widgetVisitDetails.setItem(row_count, 2, w)
            w.setText(detail["sku"])
            self.widgetVisitDetails.setItem(row_count, 3, w)
            w.setText(detail["text"])
            self.widgetVisitDetails.setItem(row_count, 4, w)
            w.setText(str(detail["price"]))
            self.widgetVisitDetails.setItem(row_count, 5, w)
            w.setText(str(detail["discount"]))
            self.widgetVisitDetails.setItem(row_count, 6, w)
            w.setText(str(detail["amount"]))
            self.widgetVisitDetails.setItem(row_count, 7, w)
            w.setText(utils.int2str_dk(detail["sas"]))
            self.widgetVisitDetails.setItem(row_count, 8, w)
            w.setText(detail["extra"])
            self.widgetVisitDetails.setItem(row_count, 9, w)

        # If customer needs special settings on prices
        factor = customers.customer["factor"]
        if factor > 0.0:
            for item in self._products:
                item["price"] = item["price"] * factor
                if not item["d2"] == 0.0:
                    item["d2"] = item["d2"] * factor
                if not item["d3"] == 0.0:
                    item["d3"] = item["d3"] * factor
                if not item["d4"] == 0.0:
                    item["d4"] = item["d4"] * factor
                if not item["d6"] == 0.0:
                    item["d6"] = item["d6"] * factor
                if not item["d8"] == 0.0:
                    item["d8"] = item["d8"] * factor
                if not item["d12"] == 0.0:
                    item["d12"] = item["d12"] * factor
                if not item["d24"] == 0.0:
                    item["d24"] = item["d24"] * factor
                if not item["d2"] == 0.0:
                    item["d48"] = item["d48"] * factor
                if not item["d96"] == 0.0:
                    item["d96"] = item["d96"] * factor
                if not item["min"] == 0.0:
                    item["min"] = item["min"] * factor
                if not item["net"] == 0.0:
                    item["net"] = item["net"] * factor
        # Set info banner
        self.txtCompany.setText(customers.customer["company"])
        # connect to signals
        self.btnAppend.clicked.connect(self.button_add_line_action)
        self.btnClear.clicked.connect(self.button_clear_line_action)
        self.btnArchiveVisit.clicked.connect(self.button_save_visit_action)
        self.cboDnst.currentIndexChanged.connect(self.dnst_changed_action)
        self.widgetVisitDetails.setColumnWidth(0, 43)   # line_type D/N/S
        self.widgetVisitDetails.setColumnWidth(1, 44)   # pcs
        self.widgetVisitDetails.setColumnWidth(2, 83)   # product
        self.widgetVisitDetails.setColumnWidth(3, 123)  # sku
        self.widgetVisitDetails.setColumnWidth(4, 153)  # text
        self.widgetVisitDetails.setColumnWidth(5, 60)   # price
        self.widgetVisitDetails.setColumnWidth(6, 50)   # discount
        self.widgetVisitDetails.setColumnWidth(7, 60)   # amount
        self.widgetVisitDetails.setColumnWidth(8, 30)   # SAS

    @pyqtSlot(name="button_clear_line_action")
    def button_clear_line_action(self):
        """
        Slot for Add Demo button clicked
        """
        pass

    @pyqtSlot(name="archive_visit")
    def archive_visit(self):
        """
        Slot for saving the visit
        """
        # save visit head contents
        self._visits.visit["po_buyer"] = self.txtPoBuyer.text()
        self._visits.visit["po_number"] = self.txtPoNumber.text()
        self._visits.visit["po_company"] = self.txtPoCompany.text()
        self._visits.visit["po_address1"] = self.txtPoAddress1.text()
        self._visits.visit["po_address2"] = self.txtPoAddress2.text()
        self._visits.visit["po_postcode"] = self.txtPoPostcode.text()
        self._visits.visit["po_postofffice"] = self.txtPoPostoffice.text()
        self._visits.visit["po_country"] = self.txtPoCountry.text()
        self._visits.visit["info_text"] = self.txtInfoText.toPlainText()
        self._visits.visit["prod_demo"] = self.txtProductDemo.text()
        self._visits.visit["prod_sale"] = self.txtProductSale.text()
        self._visits.visit["sas"] = self.txtVisitSas.text()
        self._visits.visit["sale"] = self.txtVisitSale.text()
        self._visits.visit["total"] = self.txtVisitTotal.text()

        # TODO: save visitdetails

    @pyqtSlot(name="dnst_changed_action")
    def dnst_changed_action(self):
        """
        Changed linetype
        `D`emo `N`ysalg `S`alg `T`ekst
        :return: nothing
        """
        if self.cboDnst.currentText() == "T":
            self.set_input_enabled(False)
            return
        self.set_input_enabled(True)

    def set_input_enabled(self, arg: bool):
        """Enable inputs"""
        self.txtPcs.setEnabled(arg)
        self.cboProduct.setEnabled(arg)
        self.cboSku.setEnabled(arg)
        self.txtLinePrice.setEnabled(arg)
        self.txtLineDiscount.setEnabled(arg)
        self.chkSas.setEnabled(arg)

    def load_items(self):
        """Load ITEMS into product combo"""
        for item in self._products:
            self.cboProduct.addItem(item["item"], item["sku"])

    def load_sku(self):
        """Load SKU into sku combo"""
        for item in self._products:
            self.cboProduct.addItem(item["sku"], item["name1"])

    def item_changed_action(self):
        """Update SKU combo when item changes"""
        self.cboSku.setCurrentText(self.cboProduct.itemData(self.cboProduct.currentIndex()))

    def sku_changed_action(self):
        """Update ITEM combo when sku changes"""
        self.txtLineText.setText(self.cboSku.itemData(self.cboSku.currentIndex()))
        self.cboProduct.setCurrentText(self.cboProduct.currentText())
