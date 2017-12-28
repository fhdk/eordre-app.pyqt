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
from dialogs.settings_dialog import SettingsDialog
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

        self.txtWorkdate.setText(datetime.date.today().isoformat())  # initialize workdate to current date
        self._contacts = Contact()  # Initialize Contact object
        self._customers = Customer()  # Initialize Customer object
        self._orderlines = OrderLine()  # Initialize Detail object
        self._employees = Employee()  # Initialize Employee object
        self._products = Product()  # Initialize Product object
        self._reports = Report()  # Initialize Report object
        self._visits = Visit()  # Initialize Visit object
        self._settings = Settings()  # Initialize Settings object

        # # connect menu trigger signals
        # self.actionAboutQt.triggered.connect(self.show_about_qt)
        # self.actionAboutSoftware.triggered.connect(self.show_about_software)
        # self.actionArchiveChanges.triggered.connect(self.archive_customer)
        # self.actionContactsInfo.triggered.connect(self.show_contact_data_page)
        # self.actionCreateCustomer.triggered.connect(self.create_customer)
        # self.actionCreateVisit.triggered.connect(self.show_visit_dialog)
        # self.actionImportCsvFiles.triggered.connect(self.show_csv_import_dialog)
        # self.actionExit.triggered.connect(self.app_exit_slot)
        # self.actionGetCatalogHttp.triggered.connect(self.show_http_products_dialog)
        # self.actionGetCustomersHttp.triggered.connect(self.show_http_customers_dialog)
        # self.actionMasterInfo.triggered.connect(self.show_master_data_page)
        # self.actionReport.triggered.connect(self.show_create_report_dialog)
        # self.actionReportList.triggered.connect(self.show_reports_dialog)
        # self.actionSettings.triggered.connect(self.show_settings_dialog)
        # self.actionVisitsInfo.triggered.connect(self.show_visit_data_page)
        # self.actionZeroDatabase.triggered.connect(self.zero_database)
        # # buttons on top
        # self.btnAddCustomer.clicked.connect(self.create_customer)
        # self.btnCreateReportDialog.clicked.connect(self.show_create_report_dialog)
        # # buttons for paging data
        # self.btnShowContacts.clicked.connect(self.show_contact_data_page)
        # self.btnShowMasterdata.clicked.connect(self.show_master_data_page)
        # self.btnShowVisits.clicked.connect(self.show_visit_data_page)
        # # button on master data page
        # self.btnArchiveMasterdata.clicked.connect(self.archive_customer)
        # # buttons on contacts data page
        # self.btnArchiveContacts.clicked.connect(self.archive_contacts_slot)
        # self.btnAddContact.clicked.connect(self.add_contact_slot)
        # # button visit data page
        # self.btnVisitDialog.clicked.connect(self.show_visit_dialog)
        # # connect list changes
        # self.widgetCustomerList.currentItemChanged.connect(self.on_customer_changed)
        # self.widgetVisitList.currentItemChanged.connect(self.on_visit_changed)
        # # Hide the id column on visit list
        # self.widgetVisitList.setColumnHidden(0, True)
        # # Set header on visit details
        # self.widgetVisitDetails.setColumnWidth(0, 30)
        # self.widgetVisitDetails.setColumnWidth(1, 30)
        # self.widgetVisitDetails.setColumnWidth(2, 100)
        # self.widgetVisitDetails.setColumnWidth(3, 150)
        # self.widgetVisitDetails.setColumnWidth(4, 60)
        # self.widgetVisitDetails.setColumnWidth(5, 40)
        # load report for workdate if exist
        self._reports.load_report(self.txtWorkdate.text())
        # display customerlist
        self.populate_customer_list()
        # set latest customer active
        if self._customers.lookup_by_id(self._settings.setting["cust_idx"]):
            try:
                phone = self._customers.customer["phone1"]
                self.widgetCustomerList.setCurrentIndex(
                    self.widgetCustomerList.indexFromItem(
                        self.widgetCustomerList.findItems(phone, Qt.MatchExactly, column=0)[0]))
            except KeyError:
                pass
        # set last info page used
        if self._settings.setting["page_idx"]:
            self.widgetCustomerInfo.setCurrentIndex(self._settings.setting["page_idx"])

    def closeEvent(self, event):
        """
        Slot for close event signal
        Args:
            event:

        intended use is warning about unsaved data
        """
        # TODO handle close event
        self.app_exit_slot()
        pass

    @pyqtSlot(name="app_exit_slot")
    def app_exit_slot(self):
        """
        Slot for exit triggered signal
        """
        # customer id
        try:
            self._settings.setting["cust_idx"] = self._customers.customer["customer_id"]
        except KeyError:
            self._settings.setting["cust_idx"] = 0
        # customer info page
        if not self._settings.setting["page_idx"]:
            self._settings.setting["page_idx"] = self.widgetCustomerInfo.currentIndex()
        # save setttings
        self._settings.update()
        app.quit()

    def display_sync_status(self):
        """
        Update status fields
        """
        self.txtCustLocal.setText(self._settings.setting["lsc"])
        self.txtCustServer.setText(self._settings.setting["sac"])
        self.txtProdLocal.setText(self._settings.setting["lsp"])
        self.txtProdServer.setText(self._settings.setting["sap"])

    def populate_contact_list(self):
        """
        Populate the contactlist based on currently selected customer
        """
        # load contacts
        self.widgetContactList.clear()
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

        self.widgetContactList.addTopLevelItems(items)

    def populate_customer_list(self):
        """
        Populate customer list
        """
        self.widgetCustomerList.clear()  # shake the tree for leaves
        self.widgetCustomerList.setColumnCount(4)  # set columns
        self.widgetCustomerList.setHeaderLabels(["Telefon", "Firma", "Post", "Bynavn"])
        items = []  # temporary list
        try:
            for c in self._customers.list_:
                item = QTreeWidgetItem([c["phone1"], c["company"], c["zipcode"], c["city"]])
                items.append(item)
        except (IndexError, KeyError):
            pass
        # assign Widgets to Tree
        self.widgetCustomerList.addTopLevelItems(items)
        self.widgetCustomerList.setSortingEnabled(True)  # enable sorting

    def populate_visit_details_list(self):
        """
        Populate the details list based on the line visit
        """
        self.widgetVisitDetails.clear()
        self.txtPoNumber.setText("")
        self.txtSas.setText("")
        self.txtSale.setText("")
        self.txtTotal.setText("")
        self.lblApproved.setText("")
        self.lblSent.setText("")
        self.txtVisitInfoText.setText("")

        items = []
        try:
            self._orderlines.list_ = self._visits.visit["visit_id"]

            self.txtPoNumber.setText(self._visits.visit["po_number"])
            self.txtSas.setText(str(self._visits.visit["po_sas"]))
            self.txtSale.setText(str(self._visits.visit["po_sale"]))
            self.txtTotal.setText(str(self._visits.visit["po_total"]))
            self.lblSent.setText(utils.bool2dk(utils.int2bool(self._visits.visit["po_sent"])))
            self.lblApproved.setText(utils.bool2dk(utils.int2bool(self._visits.visit["po_approved"])))
            self.txtVisitInfoText.setText(self._visits.visit["po_note"])

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
        self.widgetVisitDetails.addTopLevelItems(items)

    def populate_visit_list(self):
        """
        Populate the visitlist based on the active customer
        """
        # populate visit list table
        self.widgetVisitList.clear()
        # self.widgetVisitList.setColumnCount(5)
        self.widgetVisitList.setHeaderLabels(["Id", "Dato", "Navn", "Demo", "Salg"])
        self.widgetVisitList.setColumnWidth(0, 0)
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
        self.widgetVisitList.addTopLevelItems(items)

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

            self.show_settings_dialog()

        # if requested check server data
        if utils.int2bool(self._settings.setting["sc"]):
            # update sync status
            status = utils.refresh_sync_status(self._settings)
            self._settings.setting["sac"] = status[0][1].split()[0]
            self._settings.setting["sap"] = status[1][1].split()[0]
            self._settings.update()

        # display known sync data
        self.display_sync_status()

    @pyqtSlot(name="add_contact_slot")
    def add_contact_slot(self):
        """
        Save changes made to contacts
        """
        # TODO add new contact
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "# TODO add new contact",
                           QMessageBox.Ok)

    @pyqtSlot(name="archive_contacts_slot")
    def archive_contacts_slot(self):
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
        self._customers.customer["company"] = self.txtCompany.text()
        self._customers.customer["address1"] = self.txtAddress1.text()
        self._customers.customer["address2"] = self.txtAddress2.text()
        self._customers.customer["zipcode"] = self.txtZipCode.text()
        self._customers.customer["city"] = self.txtCityName.text()
        self._customers.customer["phone1"] = self.txtPhone1.text()
        self._customers.customer["phone2"] = self.txtPhone2.text()
        self._customers.customer["email"] = self.txtEmail.text()
        self._customers.customer["factor"] = self.txtFactor.text()
        self._customers.customer["infotext"] = self.txtCustomerInfoText.toPlainText()
        self._customers.customer["modified"] = 1
        self._customers.update()

    @pyqtSlot(name="create_customer")
    def create_customer(self):
        """
        Slot for createCustomer triggered signal
        """
        if not self.txtNewCompany.text() or not self.txtNewPhone1.text():
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
                               self.txtNewCompany.text() + "\n" +
                               self.txtNewPhone1.text(),
                               QMessageBox.Ok)

    @pyqtSlot(QTreeWidgetItem, QTreeWidgetItem, name="on_customer_changed")
    def on_customer_changed(self, current, previous):
        """
        Slot for treewidget current item changed signal
        Used to respond to changes in the currently selected current
        and update the related current info pages

        Args:
            current: currently selected item
            previous: previous selected item
        """
        try:
            phone = current.text(0)
            company = current.text(1)
            # move current customer
            # load customer
            self._customers.lookup(phone, company)
            # fields to line edits
            self.txtAccount.setText(self._customers.customer["account"])
            self.txtCompany.setText(self._customers.customer["company"])
            self.txtAddress1.setText(self._customers.customer["address1"])
            self.txtAddress2.setText(self._customers.customer["address2"])
            self.txtZipCode.setText(self._customers.customer["zipcode"])
            self.txtCityName.setText(self._customers.customer["city"])
            self.txtPhone1.setText(self._customers.customer["phone1"])
            self.txtPhone2.setText(self._customers.customer["phone2"])
            self.txtEmail.setText(self._customers.customer["email"])
            self.txtFactor.setText(str(self._customers.customer["factor"]))
            self.txtCustomerInfoText.setText(self._customers.customer["infotext"])
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
        self.txtCustLocal.setText(lsc)
        self._settings.setting["lsc"] = lsc
        self._settings.update()

    @pyqtSlot(name="on_products_done")
    def on_products_done(self):
        """
        Slot for getProducts finished signal
        """
        self._products.all()
        lsp = datetime.date.today().isoformat()
        self.txtProdLocal.setText(lsp)
        self._settings.setting["lsp"] = lsp
        self._settings.update()

    @pyqtSlot(name="on_settings_changed")
    def on_settings_changed(self):
        """
        load employee data
        :return:
        """
        self._settings.load()
        self._employees.load(self._settings.setting["usermail"])

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
        Slot for dataExport triggered signal
        """
        # TODO: Opret CSV data backup
        msgbox = QMessageBox()
        msgbox.information(self,
                           __appname__,
                           "TODO: Opret CSV data backup",
                           QMessageBox.Ok)

    @pyqtSlot(name="show_about_qt")
    def show_about_qt(self):
        """
        Slot for aboutQt triggered signal
        """
        msgbox = QMessageBox()
        msgbox.aboutQt(self, __appname__)

    @pyqtSlot(name="show_about_software")
    def show_about_software(self):
        """
        Slot for aboutSoftware triggered signal
        """
        msgbox = QMessageBox()
        msgbox.about(self, __appname__,
                     "Bygget med Python 3.6 og Qt5<br/><br/>Frede Hundewadt (c) 2017<br/><br/>"
                     "<a href='https://www.gnu.org/licenses/agpl.html'>https://www.gnu.org/licenses/agpl.html</a>")

    @pyqtSlot(name="show_contact_data_page")
    def show_contact_data_page(self):
        """
        Slot for contactData triggered signal
        """
        self.widgetCustomerInfo.setCurrentIndex(1)

    @pyqtSlot(name="show_create_report_dialog")
    def show_create_report_dialog(self):
        """
        Slot for Report triggered signal
        """
        try:
            # check the report date
            # no report triggers KeyError which in turn launches the CreateReportDialog
            repdate = self._reports.report["rep_date"]
            if not repdate == self.txtWorkdate.text():
                # if active report is not the same replace it with workdate
                self._reports.load_report(self.txtWorkdate.text())
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
            create_report_dialog = ReportDialogCreate(self.txtWorkdate.text())
            if create_report_dialog.exec_():
                # user chosed to create a report
                self.txtWorkdate.setText(create_report_dialog.workdate)
                # try load a report for that date
                self._reports.load_report(self.txtWorkdate.text())
                try:
                    # did the user choose an existing report
                    _ = self._reports.report["rep_date"]
                    infotext = "Eksisterende rapport hentet: {}".format(self.txtWorkdate.text())
                except KeyError:
                    # create the report
                    self._reports.create(self._employees.employee, self.txtWorkdate.text())
                    infotext = "Rapport oprettet for: {}".format(self.txtWorkdate.text())
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

    @pyqtSlot(name="show_http_customers_dialog")
    def show_http_customers_dialog(self):
        """
        Slot for getCustomers triggered signal
        """
        import_customers = GetCustomersHttpDialog(app,
                                                  customers=self._customers,
                                                  employees=self._employees,
                                                  settings=self._settings)
        import_customers.sig_done.connect(self.on_customers_done)
        import_customers.exec_()

    @pyqtSlot(name="show_http_products_dialog")
    def show_http_products_dialog(self):
        """
        Slot for getProducts triggered signal
        """
        import_product = GetProductsHttpDialog(app,
                                               products=self._products,
                                               settings=self._settings)
        import_product.sig_done.connect(self.on_products_done)
        import_product.exec_()

    @pyqtSlot(name="show_visit_data_page")
    def show_visit_data_page(self):
        """
        Slot for visitData triggered signal
        """
        self.widgetCustomerInfo.setCurrentIndex(2)

    @pyqtSlot(name="show_master_data_page")
    def show_master_data_page(self):
        """
        Slot for masterData triggered signal
        """
        self.widgetCustomerInfo.setCurrentIndex(0)

    @pyqtSlot(name="show_reports_dialog")
    def show_reports_dialog(self):
        """
        Slot for Report List triggered signal
        """
        pass

    @pyqtSlot(name="show_settings_dialog")
    def show_settings_dialog(self):
        """
        Slot for settingsDialog triggered signal
        """
        settings_dialog = SettingsDialog(self._settings, self._employees)
        settings_dialog.settings_changed.connect(self.on_settings_changed)
        settings_dialog.exec_()

    @pyqtSlot(name="show_visit_dialog")
    def show_visit_dialog(self):
        """
        Slot for launching the visit dialog
        """
        try:
            # do we have a report
            _ = self._reports.report["rep_date"]
            active_report = True
        except KeyError:
            active_report = self.show_create_report_dialog()

        if active_report:
            self._reports.load_report(self.txtWorkdate.text())
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

    @pyqtSlot(name="zero_database")
    def zero_database(self):
        """
        Slot for zeroDatabase triggered signal
        """
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
