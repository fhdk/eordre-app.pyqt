#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Eordre application module
"""

import datetime
import sys

from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSplashScreen, QTreeWidgetItem

from configuration import config, configfn
from dialogs.csv_import_dialog import CsvFileImportDialog
from dialogs.http_customers_dialog import GetCustomersHttpDialog
from dialogs.http_products_dialog import GetProductsHttpDialog
from dialogs.create_report_dialog import ReportDialogCreate
from dialogs.visit_dialog import VisitDialog
from models.contact import Contact
from models.customer import Customer
from models.orderline import OrderLine
from models.employee import Employee
from models.product import Product
from models.report import Report
from models.settings import Settings
from models.visit import Visit
from resources.main_window_rc import Ui_mainWindow
from resources import splash_rc
from util import utils
from util import passwdFn
from util import printFn
from util.rules import check_settings

__appname__ = "Eordre NG"
__module__ = "main.py"


class MainWindow(QMainWindow, Ui_mainWindow):
    """
    Main Application Window
    """

    def __init__(self, parent=None):
        """
        Initialize MainWindow class
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        QThread.currentThread().setObjectName(__appname__)
        configfn.check_config_folder()  # Check appdata folder in users home

        self.textWorkdate.setText(datetime.date.today().isoformat())  # initialize workdate to current date
        self._contacts = Contact()  # Initialize Contact object
        self._customers = Customer()  # Initialize Customer object
        self._orderlines = OrderLine()  # Initialize Detail object
        self._employees = Employee()  # Initialize Employee object
        self._products = Product()  # Initialize Product object
        self._reports = Report()  # Initialize Report object
        self._visits = Visit()  # Initialize Visit object
        self._settings = Settings()  # Initialize Settings object

        self.toolButtonCustomer.clicked.connect(self.show_page_customer)
        self.toolButtonCustomers.clicked.connect(self.show_page_customers)
        self.toolButtonCustomerVisits.clicked.connect(self.show_page_customer_visits)
        self.toolButtonExit.clicked.connect(self.app_exit)
        self.toolButtonInfo.clicked.connect(self.show_page_info)
        self.toolButtonPricelist.clicked.connect(self.show_page_pricelist)
        self.toolButtonReport.clicked.connect(self.show_page_report)
        self.toolButtonReports.clicked.connect(self.show_page_reports)
        self.toolButtonSettings.clicked.connect(self.show_page_settings)

        self.toolButtonImportCsvData.clicked.connect(self.show_csv_import_dialog)
        self.toolButtonDeleteSalesData.clicked.connect(self.zero_database)
        self.toolButtonExportDatabase.clicked.connect(self.data_export)
        self.toolButtonImportDatabase.clicked.connect(self.data_import)

        self.buttonGetCustomers.clicked.connect(self.get_customers)
        self.buttonGetPricelist.clicked.connect(self.get_pricelist)
        self.buttonCreateReport.clicked.connect(self.create_report)

        self.buttonArchiveContacts.clicked.connect(self.archive_contacts)
        self.buttonArchiveCustomer.clicked.connect(self.archive_customer)
        self.buttonCreateContact.clicked.connect(self.create_contact)
        self.buttonCreateCustomer.clicked.connect(self.create_customer)
        self.buttonCreateVisit.clicked.connect(self.create_visit)

        self.widgetAppCustomers.currentItemChanged.connect(self.on_customer_changed)
        self.widgetAppCustomers.itemDoubleClicked.connect(self.on_customer_double_clicked)
        self.widgetCustomerVisits.currentItemChanged.connect(self.on_visit_changed)
        self.widgetCustomerVisits.setColumnHidden(0, True)

        self.widgetSingleVisitDetails.setColumnWidth(0, 30)
        self.widgetSingleVisitDetails.setColumnWidth(1, 30)
        self.widgetSingleVisitDetails.setColumnWidth(2, 100)
        self.widgetSingleVisitDetails.setColumnWidth(3, 150)
        self.widgetSingleVisitDetails.setColumnWidth(4, 60)
        self.widgetSingleVisitDetails.setColumnWidth(5, 40)

        # load report for workdate if exist
        self._reports.load_report(self.textWorkdate.text())
        # fill customer list
        self.populate_customer_list()
        # set latest customer active
        if self._customers.lookup_by_id(self._settings.setting["cust_idx"]):
            try:
                phone = self._customers.customer["phone1"]
                self.widgetAppCustomers.setCurrentIndex(
                    self.widgetAppCustomers.indexFromItem(
                        self.widgetAppCustomers.findItems(phone, Qt.MatchExactly, column=1)[0]))
                self.toolButtonCustomer.click()
                return
            except KeyError:
                pass
        self.toolButtonCustomers.click()

    def closeEvent(self, event):
        """
        Slot for close event signal
        Args:
            event:

        intended use is warning about unsaved data
        """
        # TODO handle close event
        self.app_exit()

    @pyqtSlot(name="app_exit")
    def app_exit(self):
        """
        Exit - save current customer
        """
        # customer id
        try:
            self._settings.setting["cust_idx"] = self._customers.customer["customer_id"]
        except KeyError:
            self._settings.setting["cust_idx"] = 0
        # if not self._settings.setting["page_idx"]:
        #     self._settings.setting["page_idx"] = self.widgetAppPages.currentIndex()
        # save setttings
        self._settings.update()
        app.quit()

    def display_sync_status(self):
        """
        Update status fields
        """
        self.textCustomerLocalDate.setText(self._settings.setting["lsc"])
        self.textCustomerServerDate.setText(self._settings.setting["sac"])
        self.textPricelistLocalDate.setText(self._settings.setting["lsp"])
        self.textPricelistServerDate.setText(self._settings.setting["sap"])

    def populate_contact_list(self):
        """
        Populate the contactlist based on currently selected customer
        """
        # load contacts
        self.widgetCustomerContacts.clear()
        items = []
        try:
            self._contacts.list_ = self._customers.customer["customer_id"]
            for c in self._contacts.list_:
                item = QTreeWidgetItem([c["name"],
                                        c["department"],
                                        c["phone"],
                                        c["email"]])
                items.append(item)
        except IndexError:
            pass
        except KeyError:
            pass

        self.widgetCustomerContacts.addTopLevelItems(items)

    def populate_customer_list(self):
        """
        Populate customer list
        """

        self.widgetAppCustomers.clear()  # shake the tree for leaves
        self.widgetAppCustomers.setColumnCount(6)  # set columns
        self.widgetAppCustomers.setHeaderLabels(["Konto", "Telefon", "Telefon", "Firma", "Post", "Bynavn"])
        items = []  # temporary list
        try:
            for c in self._customers.list_:
                item = QTreeWidgetItem([c["account"], c["phone1"], c["phone2"], c["company"], c["zipcode"], c["city"]])
                items.append(item)
        except (IndexError, KeyError):
            pass
        # assign Widgets to Tree
        self.widgetAppCustomers.addTopLevelItems(items)
        self.widgetAppCustomers.setSortingEnabled(True)  # enable sorting

    def populate_price_list(self):
        """
        Populate the visitlist based on the active customer
        """
        # populate visit list table
        self.widgetCustomerVisits.setHeaderLabels(["Id", "Dato", "Navn", "Demo", "Salg"])
        self.widgetCustomerVisits.setColumnWidth(0, 0)
        items = []
        try:
            self._visits.list_customer = self._customers.customer["customer_id"]
            for visit in self._visits.list_customer:
                item = QTreeWidgetItem([str(visit["visit_id"]),
                                        visit["visit_date"],
                                        visit["po_buyer"],
                                        visit["prod_demo"],
                                        visit["prod_sale"]])
                items.append(item)
        except IndexError:
            pass
        except KeyError:
            pass
        self.widgetCustomerVisits.addTopLevelItems(items)

    def populate_settings_page(self):
        """
        Populate settings page
        :return: 
        """
        self.textAppUserMail.setText(self._settings.setting["usermail"])
        self.textAppUserPass.setText(self._settings.setting["userpass"])
        self.textAppUserCountry.setText(self._settings.setting["usercountry"])
        self.textAppDataServer.setText(self._settings.setting["http"])
        self.textAppMailServer.setText(self._settings.setting["smtp"])
        self.textAppMailServerPort.setText(str(self._settings.setting["port"]))
        self.textAppMailOrderTo.setText(self._settings.setting["mailto"])
        self.checkServerData.setChecked(utils.int2bool(self._settings.setting["sc"]))
        self.textExtMailServer.setText(self._settings.setting["mailserver"])
        self.textExtMailServerPort.setText(str(self._settings.setting["mailport"]))
        self.textExtMailServerUser.setText(self._settings.setting["mailuser"])
        self.textExtMailServerPass.setText(self._settings.setting["mailpass"])

    def populate_visit_details_list(self):
        """
        Populate the details list based on the line visit
        """
        self.widgetSingleVisitDetails.clear()
        self.textArchivePoNumber.setText("")
        self.textArchiveSas.setText("")
        self.textArchiveSale.setText("")
        self.textArchiveTotal.setText("")
        self.labelArchiveApprovedText.setText("")
        self.labelArchiveSendText.setText("")
        self.textSingleVisitNotes.setText("")

        items = []
        try:
            self._orderlines.list_ = self._visits.visit["visit_id"]

            self.textArchivePoNumber.setText(self._visits.visit["po_number"])
            self.textArchiveSas.setText(str(self._visits.visit["po_sas"]))
            self.textArchiveSale.setText(str(self._visits.visit["po_sale"]))
            self.textArchiveTotal.setText(str(self._visits.visit["po_total"]))
            self.labelArchiveSendText.setText(utils.bool2dk(utils.int2bool(self._visits.visit["po_sent"])))
            self.labelArchiveApprovedText.setText(utils.bool2dk(utils.int2bool(self._visits.visit["po_approved"])))
            self.textSingleVisitNotes.setText(self._visits.visit["po_note"])

            for detail in self._orderlines.list_:
                item = QTreeWidgetItem([detail["linetype"],
                                        str(detail["pcs"]),
                                        detail["sku"],
                                        detail["text"],
                                        str(detail["price"]),
                                        str(detail["discount"]),
                                        detail["extra"]])
                items.append(item)
        except KeyError:
            pass
        except IndexError:
            pass
        self.widgetSingleVisitDetails.addTopLevelItems(items)

    def populate_visit_list(self):
        """
        Populate the visitlist based on the active customer
        """
        # populate visit list table
        self.widgetCustomerVisits.clear()
        # self.widgetCustomerVisits.setColumnCount(5)
        self.widgetCustomerVisits.setHeaderLabels(["Id", "Dato", "Navn", "Demo", "Salg"])
        self.widgetCustomerVisits.setColumnWidth(0, 0)
        items = []
        try:
            self._visits.list_customer = self._customers.customer["customer_id"]
            for visit in self._visits.list_customer:
                item = QTreeWidgetItem([str(visit["visit_id"]),
                                        visit["visit_date"],
                                        visit["po_buyer"],
                                        visit["prod_demo"],
                                        visit["prod_sale"]])
                items.append(item)
        except IndexError:
            pass
        except KeyError:
            pass
        self.widgetCustomerVisits.addTopLevelItems(items)

    def resizeEvent(self, event):
        """
        Slot for the resize event signal
        Args:
            event:
        intended use is resize content to window
        :param event:
        """
        # TODO handle resize event
        pass

    def run(self):
        """
        Setup database and basic configuration
        """
        # basic settings must be done
        is_set = check_settings(self._settings.setting)
        if is_set:
            try:
                _ = self._employees.employee["fullname"]
            except KeyError:
                msgbox = QMessageBox()
                msgbox.about(self,
                             __appname__,
                             "Der er en fejl i dine indstillinger.\nKontroller dem venligst.\nTak.")
        else:
            msgbox = QMessageBox()
            msgbox.about(self,
                         __appname__,
                         "App'en skal bruge nogle oplysninger.\nRing kontoret hvis du er i tvivl.\nTak.")

            self.show_page_settings()

        # if requested check server data
        if utils.int2bool(self._settings.setting["sc"]):
            # update sync status
            status = utils.refresh_sync_status(self._settings)
            self._settings.setting["sac"] = status[0][1].split()[0]
            self._settings.setting["sap"] = status[1][1].split()[0]
            self._settings.update()

        # display known sync data
        self.display_sync_status()

    def update_page_settings(self, button: str):
        """
        Save page index to settings
        :param button:
        :return:
        """
        # customer id
        try:
            self._settings.setting["cust_idx"] = self._customers.customer["customer_id"]
        except KeyError:
            self._settings.setting["cust_idx"] = 0
        if not self._settings.setting["page_idx"]:
            self._settings.setting["page_idx"] = self.widgetAppPages.currentIndex()
        self._settings.setting["toolbutton"] = button
        self._settings.update()

    @pyqtSlot(name="create_contact")
    def create_contact(self):
        """
        Save changes made to contacts
        """
        # TODO add new contact
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "# TODO add new contact",
                           QMessageBox.Ok)

    @pyqtSlot(name="archive_contacts")
    def archive_contacts(self):
        """
        Save changes made to contacts
        """
        # TODO save changes made to contacts
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "# TODO save changes made to contacts",
                           QMessageBox.Ok)

    @pyqtSlot(name="archive_customer")
    def archive_customer(self):
        """
        Slot for updateCustomer triggered signal
        """
        if not self._customers.customer:
            # msgbox triggered if no current is selected
            msgbox = QMessageBox()
            msgbox.information(self,
                               __appname__,
                               "Det kan jeg ikke på nuværende tidspunkt!",
                               QMessageBox.Ok)
            return False
        # assign input field values to current object
        self._customers.customer["company"] = self.textCompany.text()
        self._customers.customer["address1"] = self.textAddress1.text()
        self._customers.customer["address2"] = self.textAddress2.text()
        self._customers.customer["zipcode"] = self.textZipCode.text()
        self._customers.customer["city"] = self.textCityName.text()
        self._customers.customer["phone1"] = self.textPhone1.text()
        self._customers.customer["phone2"] = self.textPhone2.text()
        self._customers.customer["email"] = self.textEmail.text()
        self._customers.customer["factor"] = self.textFactor.text()
        self._customers.customer["infotext"] = self.textCustomerInfoText.toPlainText()
        self._customers.customer["modified"] = 1
        self._customers.update()

    @pyqtSlot(name="archive_settings")
    def archive_settings(self):
        """
        Archive settings
        :return:
        """
        checkok = True
        items = []
        if self.textAppUserMail.text() == "":
            items.append("Gruppe 'Sælger' -> 'Email'")
            checkok = False
        if self.textAppUserPass.text() == "":
            items.append("Gruppe 'Sælger' -> 'Adgangsfrase'")
            checkok = False
        if self.textAppUserCountry.text() == "":
            items.append("Gruppe: Sælger -> landekode")
            checkok = False
        if self.textAppMailServer.text() == "":
            items.append("Gruppe: Intern -> Mailserver")
            checkok = False
        if self.textAppMailServerPort.text() == "":
            items.append("Gruppe: Intern -> Port")
            checkok = False
        if self.textAppMailOrderTo == "":
            items.append("Gruppe: Intern -> Mail til")
            checkok = False
        if self.textAppDataServer == "":
            items.append("Gruppe: Intern -> Dataserver")
            checkok = False
        # inform user about settings validity
        if not checkok:
            msgbox = QMessageBox()
            msgbox.warning(self, "Eordre",
                           "Der er mangler i dine indstillinger!\n{}".format("\n".join(items)),
                           QMessageBox.Ok)
            return False
        # update password in settings
        if len(self.textAppUserPass.text()) < 97:
            self._settings.setting["userpass"] = passwdFn.hash_password(self.textAppUserPass.text())
        if len(self.textExtMailServerPass) < 97:
            self._settings.setting["mailpass"] = passwdFn.hash_password(self.textExtMailServerPass.text())
        self._settings.setting["usermail"] = self.textAppUserMail.text().lower()
        self._settings.setting["usercountry"] = self.textAppUserCountry.text()
        self._settings.setting["http"] = self.textAppDataServer.text()
        self._settings.setting["smtp"] = self.textAppMailServer.text()
        self._settings.setting["port"] = self.textAppMailServerPort.text()
        self._settings.setting["mailto"] = self.textAppMailOrderTo.text()
        self._settings.setting["sc"] = utils.bool2int(self.checkServerData.isChecked())
        self._settings.setting["mailserver"] = self.textExtMailServer.text().lower()
        self._settings.setting["mailport"] = self.textExtMailServerPort.text()
        self._settings.setting["mailuser"] = self.textExtMailServerUser.text()
        self._settings.update()
        # self._settings.load()
        self._employees.load(self._settings.setting["usermail"])

    @pyqtSlot(name="create_customer")
    def create_customer(self):
        """
        Slot for createCustomer triggered signal
        """
        if not self.textNewCompany.text() or not self.textNewPhone1.text():
            msgbox = QMessageBox()
            msgbox.information(self,
                               __appname__,
                               "Snap - Jeg mangler:\n Firma navn \n Telefon nummer",
                               QMessageBox.Ok)
        else:
            msgbox = QMessageBox()
            msgbox.information(self,
                               __appname__,
                               "Gem kunde til database\n\n" +
                               self.textNewCompany.text() + "\n" +
                               self.textNewPhone1.text(),
                               QMessageBox.Ok)

    @pyqtSlot(name="create_visit")
    def create_visit(self):
        """
        Slot for launching the visit dialog
        """
        try:
            # do we have a report
            _ = self._reports.report["rep_date"]
            active_report = True
        except KeyError:
            active_report = self.create_report()

        if active_report:
            self._reports.load_report(self.textWorkdate.text())
            try:
                # do we have a customer
                _ = self._customers.customer["company"]
            except KeyError:
                msgbox = QMessageBox()
                msgbox.information(self,
                                   __appname__,
                                   "Ingen valgt kunde! Besøg kan ikke oprettes.",
                                   QMessageBox.Ok)
                return
            # Launch the visit dialog
            visit_dialog = VisitDialog(customers=self._customers,
                                       employees=self._employees,
                                       products=self._products,
                                       reports=self._reports,
                                       visits=self._visits)
            if visit_dialog.exec_():
                pass

    @pyqtSlot(QTreeWidgetItem, name="on_customer_clicked")
    def on_customer_double_clicked(self, current):
        """
        Customer selected in
        :param current:
        :return:
        """
        self.toolButtonCustomer.click()

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem, name="on_customer_changed")
    def on_customer_changed(self, current, previous):
        """
        Slot for treewidget current item changed signal
        Used to respond to changes in the customer list
        and update the related customer info

        Args:
            current: currently selected item
            previous: previous selected item
        """
        try:
            # account = current.text(0)
            phone = current.text(1)
            company = current.text(3)
            # move current customer
            # load customer
            self._customers.lookup(phone, company)
            # fields to line edits
            self.textAccount.setText(self._customers.customer["account"])
            self.textCompany.setText(self._customers.customer["company"])
            self.textAddress1.setText(self._customers.customer["address1"])
            self.textAddress2.setText(self._customers.customer["address2"])
            self.textZipCode.setText(self._customers.customer["zipcode"])
            self.textCityName.setText(self._customers.customer["city"])
            self.textPhone1.setText(self._customers.customer["phone1"])
            self.textPhone2.setText(self._customers.customer["phone2"])
            self.textEmail.setText(self._customers.customer["email"])
            self.textFactor.setText(str(self._customers.customer["factor"]))
            self.textCustomerInfoText.setText(self._customers.customer["infotext"])
        except AttributeError:
            pass
        except KeyError:
            pass
        # load customer infos
        self.populate_contact_list()
        self.populate_visit_list()
        self.populate_visit_details_list()

    @pyqtSlot(name="on_csv_import_done")
    def on_csv_import_done(self):
        """
        Slog for csv import done signal
        """
        self.populate_customer_list()

    @pyqtSlot(name="on_customers_done")
    def on_customers_done(self):
        """
        Slot for getCustomers finished signal
        """
        self.populate_customer_list()
        lsc = datetime.date.today().isoformat()
        self.textCustomerLocalDate.setText(lsc)
        self._settings.setting["lsc"] = lsc
        self._settings.update()

    @pyqtSlot(name="on_products_done")
    def on_products_done(self):
        """
        Slot for getProducts finished signal
        """
        self._products.all()
        lsp = datetime.date.today().isoformat()
        self.textPricelistLocalDate.setText(lsp)
        self._settings.setting["lsp"] = lsp
        self._settings.update()

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem, name="on_visit_changed")
    def on_visit_changed(self, current, previous):
        """
        Response to current visit changed
        Args:
            current:
            previous:
        """
        try:
            self._visits.visit = current.text(0)
        except AttributeError:
            pass
        except KeyError:
            pass
        self.populate_visit_details_list()

    @pyqtSlot(name="data_export")
    def data_export(self):
        """
        Export Database backup file
        """
        # TODO: Opret CSV data backup
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "TODO: Create Database Backup File",
                           QMessageBox.Ok)

    @pyqtSlot(name="data_import")
    def data_import(self):
        """
        Import Database backup file
        """
        # TODO: Opret CSV data backup
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "TODO: Import Database Backup File",
                           QMessageBox.Ok)

    @pyqtSlot(name="create_report")
    def create_report(self):
        """
        Slot for Report triggered signal
        """
        try:
            # check the report date
            # no report triggers KeyError which in turn launches the CreateReportDialog
            repdate = self._reports.report["rep_date"]
            if not repdate == self.textWorkdate.text():
                # if active report is not the same replace it with workdate
                self._reports.load_report(self.textWorkdate.text())
                # trigger a KeyError if no report is current which launches the CreateReportDialog
                repdate = self._reports.report["rep_date"]
                # check if the report is sent
                if self._reports.report["sent"] == 1:
                    # we do not allow visits to be created on a report which is closed
                    self.buttonCreateVisit.setEnabled(False)
                else:
                    self.buttonCreateVisit.setEnabled(True)
            infotext = "Rapport aktiv for: {}".format(repdate)
            msgbox = QMessageBox()
            msgbox.information(self, __appname__, infotext, QMessageBox.Ok)
            return True

        except KeyError:
            # Show report dialog
            create_report_dialog = ReportDialogCreate(self.textWorkdate.text())
            if create_report_dialog.exec_():
                # user chosed to create a report
                self.textWorkdate.setText(create_report_dialog.workdate)
                # try load a report for that date
                self._reports.load_report(self.textWorkdate.text())
                try:
                    # did the user choose an existing report
                    _ = self._reports.report["rep_date"]
                    infotext = "Eksisterende rapport hentet: {}".format(self.textWorkdate.text())
                except KeyError:
                    # create the report
                    self._reports.create(self._employees.employee, self.textWorkdate.text())
                    infotext = "Rapport oprettet for: {}".format(self.textWorkdate.text())
                msgbox = QMessageBox()
                msgbox.information(self, __appname__, infotext, QMessageBox.Ok)
                return True
            else:
                msgbox = QMessageBox()
                msgbox.information(self,
                                   __appname__,
                                   "Den aktive rapport er <strong>IKKE</strong> ændret!",
                                   QMessageBox.Ok)
                return False

    @pyqtSlot(name="shoq_csv_import_dialog")
    def show_csv_import_dialog(self):
        """
        Slot for fileImport triggered signal
        """
        if self._customers.list_:
            msgbox = QMessageBox()
            msgbox.warning(self,
                           __appname__,
                           "<strong>Ved import slettes alle eksisterende data</strong>!<br/><br/>"
                           "Det er alt eller intet af hensyn til datas sammenhæng.<br/>"
                           "Du <strong>SKAL</strong> importere <strong>ALLE<strong> tabeller fra listen!<br/><br/>"
                           "<strong>Gør du ikke det giver det uløselige problemer</strong>!",
                           QMessageBox.Ok)
        # app, contact, customer, detail, employee, report, visit, tables
        import_dialog = CsvFileImportDialog(app, contacts=self._contacts, customers=self._customers,
                                            employees=self._employees, orderlines=self._orderlines,
                                            reports=self._reports, tables=config.CSV_TABLES, visits=self._visits)
        import_dialog.sig_done.connect(self.on_csv_import_done)
        import_dialog.exec_()

    @pyqtSlot(name="get_customers")
    def get_customers(self):
        """
        Slot for getCustomers triggered signal
        """
        import_customers = GetCustomersHttpDialog(app,
                                                  customers=self._customers,
                                                  employees=self._employees,
                                                  settings=self._settings)
        import_customers.sig_done.connect(self.on_customers_done)
        import_customers.exec_()

    @pyqtSlot(name="get_pricelist")
    def get_pricelist(self):
        """
        Slot for getProducts triggered signal
        """
        import_product = GetProductsHttpDialog(app,
                                               products=self._products,
                                               settings=self._settings)
        import_product.sig_done.connect(self.on_products_done)
        import_product.exec_()

    @pyqtSlot(name="show_page_customers")
    def show_page_customers(self):
        """
        Show page with customer list
        """
        self.update_page_settings(button="toolButtonCustomers")
        self.widgetAppPages.setCurrentIndex(0)

    @pyqtSlot(name="show_page_customer")
    def show_page_customer(self):
        """
        Show page with customer
        """
        self.update_page_settings(button="toolButtonCustomer")
        self.widgetAppPages.setCurrentIndex(1)

    @pyqtSlot(name="show_page_customer_visits")
    def show_page_customer_visits(self):
        """
        Show page with customer visits and orders
        """
        self.update_page_settings(button="toolButtonCustomerVisits")
        self.widgetAppPages.setCurrentIndex(2)

    @pyqtSlot(name="show_page_pricelist")
    def show_page_pricelist(self):
        """
        Show page with pricelist
        """
        self.update_page_settings(button="toolButtonPricelist")
        self.widgetAppPages.setCurrentIndex(3)

    @pyqtSlot(name="show_page_report")
    def show_page_report(self):
        """
        Slot for masterData triggered signal
        """
        self.update_page_settings(button="toolButtonReport")
        self.widgetAppPages.setCurrentIndex(4)

    @pyqtSlot(name="show_page_reports")
    def show_page_reports(self):
        """
        Show page with a report list
        """
        self.update_page_settings(button="toolButtonReports")
        self.widgetAppPages.setCurrentIndex(5)

    @pyqtSlot(name="show_page_settings")
    def show_page_settings(self):
        """
        Show page with settings
        """
        self.update_page_settings(button="toolButtonSettings")
        self.populate_settings_page()
        self.widgetAppPages.setCurrentIndex(6)

    @pyqtSlot(name="show_page_info")
    def show_page_info(self):
        """
        Show page with about Qt and Eordre
        """
        self.update_page_settings(button="toolButtonInfo")
        self.widgetAppPages.setCurrentIndex(7)

    @pyqtSlot(name="zero_database")
    def zero_database(self):
        """
        Slot for zeroDatabase triggered signal
        """
        confirm = QMessageBox()
        val = confirm.question(self, __appname__, "Alle salgsdata slettes<br/>Vil du fortsætte?", confirm.Yes | confirm.No)

        if val == confirm.Yes:
            self._contacts.recreate_table()
            self._customers.recreate_table()
            self._orderlines.recreate_table()
            self._visits.recreate_table()
            self._reports.recreate_table()

            self.populate_contact_list()
            self.populate_visit_details_list()
            self.populate_visit_list()
            self.populate_customer_list()

            self._settings.setting["lsc"] = ""
            self._settings.setting["sac"] = ""
            self._settings.setting["lsp"] = ""
            self._settings.setting["sap"] = ""
            self._settings.update()
            self.display_sync_status()

            msgbox = QMessageBox()
            msgbox.information(self, __appname__, "Salgsdata er nulstillet!", QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setAutoSipEnabled(True)
    # app.setDesktopSettingsAware(True)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling)

    pixmap = QPixmap(":/splash/splash.png")
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()

    app.processEvents()

    window = MainWindow()
    window.show()

    QTimer.singleShot(1000, window.run)
    splash.finish(window)

    sys.exit(app.exec_())
