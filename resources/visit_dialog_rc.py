# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VisitDialog(object):
    def setupUi(self, VisitDialog):
        VisitDialog.setObjectName("VisitDialog")
        VisitDialog.resize(636, 568)
        self.formLayoutWidget = QtWidgets.QWidget(VisitDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 60, 321, 252))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formVisit = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formVisit.setContentsMargins(0, 0, 0, 0)
        self.formVisit.setObjectName("formVisit")
        self.txtOrderVisitDate = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtOrderVisitDate.setEnabled(False)
        self.txtOrderVisitDate.setObjectName("txtOrderVisitDate")
        self.formVisit.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtOrderVisitDate)
        self.txtBuyer = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtBuyer.setObjectName("txtBuyer")
        self.formVisit.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtBuyer)
        self.txtPurchaseOrder = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtPurchaseOrder.setObjectName("txtPurchaseOrder")
        self.formVisit.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtPurchaseOrder)
        self.txtProductDemo = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtProductDemo.setObjectName("txtProductDemo")
        self.formVisit.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txtProductDemo)
        self.txtProductSale = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.txtProductSale.setObjectName("txtProductSale")
        self.formVisit.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txtProductSale)
        self.txtNote = QtWidgets.QTextEdit(self.formLayoutWidget)
        self.txtNote.setObjectName("txtNote")
        self.formVisit.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txtNote)
        self.orderLinesWidget = QtWidgets.QTableWidget(VisitDialog)
        self.orderLinesWidget.setGeometry(QtCore.QRect(10, 320, 620, 192))
        self.orderLinesWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.orderLinesWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.orderLinesWidget.setObjectName("orderLinesWidget")
        self.orderLinesWidget.setColumnCount(8)
        self.orderLinesWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.orderLinesWidget.setHorizontalHeaderItem(7, item)
        self.orderLinesWidget.horizontalHeader().setDefaultSectionSize(70)
        self.orderLinesWidget.horizontalHeader().setMinimumSectionSize(10)
        self.orderLinesWidget.verticalHeader().setStretchLastSection(True)
        self.formLayoutWidget_2 = QtWidgets.QWidget(VisitDialog)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(339, 60, 291, 206))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formDeliveryAddress = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formDeliveryAddress.setContentsMargins(0, 0, 0, 0)
        self.formDeliveryAddress.setObjectName("formDeliveryAddress")
        self.txtDeliverCompany = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtDeliverCompany.setObjectName("txtDeliverCompany")
        self.formDeliveryAddress.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.txtDeliverCompany)
        self.txtDeliverAddress1 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtDeliverAddress1.setObjectName("txtDeliverAddress1")
        self.formDeliveryAddress.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.txtDeliverAddress1)
        self.txtDeliverAddress2 = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtDeliverAddress2.setObjectName("txtDeliverAddress2")
        self.formDeliveryAddress.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txtDeliverAddress2)
        self.txtZipCode = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtZipCode.setObjectName("txtZipCode")
        self.formDeliveryAddress.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.txtZipCode)
        self.txtCityName = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtCityName.setObjectName("txtCityName")
        self.formDeliveryAddress.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.txtCityName)
        self.txtDeliverCountry = QtWidgets.QLineEdit(self.formLayoutWidget_2)
        self.txtDeliverCountry.setObjectName("txtDeliverCountry")
        self.formDeliveryAddress.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.txtDeliverCountry)
        self.gridLayoutWidget = QtWidgets.QWidget(VisitDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(340, 280, 290, 31))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridOrderTotals = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridOrderTotals.setContentsMargins(0, 0, 0, 0)
        self.gridOrderTotals.setObjectName("gridOrderTotals")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridOrderTotals.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridOrderTotals.addWidget(self.label_2, 1, 2, 1, 1)
        self.txtOrderSale = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtOrderSale.setEnabled(False)
        self.txtOrderSale.setObjectName("txtOrderSale")
        self.gridOrderTotals.addWidget(self.txtOrderSale, 1, 1, 1, 1)
        self.txtOrderSas = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtOrderSas.setEnabled(False)
        self.txtOrderSas.setObjectName("txtOrderSas")
        self.gridOrderTotals.addWidget(self.txtOrderSas, 1, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridOrderTotals.addWidget(self.label_3, 1, 4, 1, 1)
        self.txtOrderTotal = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txtOrderTotal.setEnabled(False)
        self.txtOrderTotal.setObjectName("txtOrderTotal")
        self.gridOrderTotals.addWidget(self.txtOrderTotal, 1, 5, 1, 1)
        self.line = QtWidgets.QFrame(VisitDialog)
        self.line.setGeometry(QtCore.QRect(330, 60, 16, 240))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayoutWidget_2 = QtWidgets.QWidget(VisitDialog)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 621, 35))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridOrderVisitAt = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridOrderVisitAt.setContentsMargins(0, 0, 0, 0)
        self.gridOrderVisitAt.setObjectName("gridOrderVisitAt")
        self.lblCompany = QtWidgets.QLabel(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lblCompany.setFont(font)
        self.lblCompany.setObjectName("lblCompany")
        self.gridOrderVisitAt.addWidget(self.lblCompany, 0, 0, 1, 1)
        self.txtCompany = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.txtCompany.setFont(font)
        self.txtCompany.setObjectName("txtCompany")
        self.gridOrderVisitAt.addWidget(self.txtCompany, 0, 1, 1, 1)
        self.gridLayoutWidget_3 = QtWidgets.QWidget(VisitDialog)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 520, 621, 41))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridOrderButtons = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridOrderButtons.setContentsMargins(0, 0, 0, 0)
        self.gridOrderButtons.setObjectName("gridOrderButtons")
        self.buttonAddOrderLine = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.buttonAddOrderLine.setDefault(True)
        self.buttonAddOrderLine.setObjectName("buttonAddOrderLine")
        self.gridOrderButtons.addWidget(self.buttonAddOrderLine, 0, 0, 1, 1)
        self.buttonCreateOrderVisit = QtWidgets.QPushButton(self.gridLayoutWidget_3)
        self.buttonCreateOrderVisit.setObjectName("buttonCreateOrderVisit")
        self.gridOrderButtons.addWidget(self.buttonCreateOrderVisit, 0, 1, 1, 1)

        self.retranslateUi(VisitDialog)
        QtCore.QMetaObject.connectSlotsByName(VisitDialog)
        VisitDialog.setTabOrder(self.txtOrderVisitDate, self.txtBuyer)
        VisitDialog.setTabOrder(self.txtBuyer, self.txtPurchaseOrder)
        VisitDialog.setTabOrder(self.txtPurchaseOrder, self.txtProductDemo)
        VisitDialog.setTabOrder(self.txtProductDemo, self.txtProductSale)
        VisitDialog.setTabOrder(self.txtProductSale, self.txtNote)
        VisitDialog.setTabOrder(self.txtNote, self.txtDeliverCompany)
        VisitDialog.setTabOrder(self.txtDeliverCompany, self.txtDeliverAddress1)
        VisitDialog.setTabOrder(self.txtDeliverAddress1, self.txtDeliverAddress2)
        VisitDialog.setTabOrder(self.txtDeliverAddress2, self.txtZipCode)
        VisitDialog.setTabOrder(self.txtZipCode, self.txtCityName)
        VisitDialog.setTabOrder(self.txtCityName, self.txtDeliverCountry)
        VisitDialog.setTabOrder(self.txtDeliverCountry, self.txtOrderSale)
        VisitDialog.setTabOrder(self.txtOrderSale, self.txtOrderSas)
        VisitDialog.setTabOrder(self.txtOrderSas, self.txtOrderTotal)
        VisitDialog.setTabOrder(self.txtOrderTotal, self.orderLinesWidget)
        VisitDialog.setTabOrder(self.orderLinesWidget, self.buttonAddOrderLine)

    def retranslateUi(self, VisitDialog):
        _translate = QtCore.QCoreApplication.translate
        VisitDialog.setWindowTitle(_translate("VisitDialog", "Besøg / Indkøbs ordre"))
        self.txtOrderVisitDate.setPlaceholderText(_translate("VisitDialog", "Ordre dato"))
        self.txtBuyer.setPlaceholderText(_translate("VisitDialog", "Indkøber"))
        self.txtPurchaseOrder.setPlaceholderText(_translate("VisitDialog", "Rekvisition"))
        self.txtProductDemo.setPlaceholderText(_translate("VisitDialog", "Produkt demo"))
        self.txtProductSale.setPlaceholderText(_translate("VisitDialog", "Produkt salg"))
        item = self.orderLinesWidget.horizontalHeaderItem(0)
        item.setText(_translate("VisitDialog", "Antal"))
        item = self.orderLinesWidget.horizontalHeaderItem(1)
        item.setText(_translate("VisitDialog", "Produkt"))
        item = self.orderLinesWidget.horizontalHeaderItem(2)
        item.setText(_translate("VisitDialog", "Varenr"))
        item = self.orderLinesWidget.horizontalHeaderItem(3)
        item.setText(_translate("VisitDialog", "Tekst"))
        item = self.orderLinesWidget.horizontalHeaderItem(4)
        item.setText(_translate("VisitDialog", "Pris"))
        item = self.orderLinesWidget.horizontalHeaderItem(5)
        item.setText(_translate("VisitDialog", "%"))
        item = self.orderLinesWidget.horizontalHeaderItem(6)
        item.setText(_translate("VisitDialog", "Beløb"))
        item = self.orderLinesWidget.horizontalHeaderItem(7)
        item.setText(_translate("VisitDialog", "SAS"))
        self.txtDeliverCompany.setPlaceholderText(_translate("VisitDialog", "Leveres til"))
        self.txtDeliverAddress1.setPlaceholderText(_translate("VisitDialog", "Leverings adresse 1"))
        self.txtDeliverAddress2.setPlaceholderText(_translate("VisitDialog", "Leverings adresse 2"))
        self.txtZipCode.setPlaceholderText(_translate("VisitDialog", "Leverings adresse postnummer"))
        self.txtCityName.setPlaceholderText(_translate("VisitDialog", "Leverings adresse bynavn"))
        self.txtDeliverCountry.setPlaceholderText(_translate("VisitDialog", "Leverings adresse land"))
        self.label.setText(_translate("VisitDialog", "Salg"))
        self.label_2.setText(_translate("VisitDialog", "SAS"))
        self.label_3.setText(_translate("VisitDialog", "Total"))
        self.lblCompany.setText(_translate("VisitDialog", "Besøg / Ordre:"))
        self.buttonAddOrderLine.setText(_translate("VisitDialog", "Ny ordrelinje"))
        self.buttonCreateOrderVisit.setText(_translate("VisitDialog", "Arkiver"))

