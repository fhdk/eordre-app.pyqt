# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_customers_http_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_getCustomersHttpDialog(object):
    def setupUi(self, getCustomersHttpDialog):
        getCustomersHttpDialog.setObjectName("getCustomersHttpDialog")
        getCustomersHttpDialog.resize(540, 109)
        self.itemList = QtWidgets.QListWidget(getCustomersHttpDialog)
        self.itemList.setGeometry(QtCore.QRect(10, 10, 351, 60))
        self.itemList.setObjectName("itemList")
        self.progress_bar = QtWidgets.QProgressBar(getCustomersHttpDialog)
        self.progress_bar.setGeometry(QtCore.QRect(10, 80, 521, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.buttonStart = QtWidgets.QPushButton(getCustomersHttpDialog)
        self.buttonStart.setGeometry(QtCore.QRect(370, 10, 161, 26))
        self.buttonStart.setObjectName("buttonStart")
        self.buttonClose = QtWidgets.QPushButton(getCustomersHttpDialog)
        self.buttonClose.setGeometry(QtCore.QRect(370, 40, 161, 26))
        self.buttonClose.setObjectName("buttonClose")

        self.retranslateUi(getCustomersHttpDialog)
        QtCore.QMetaObject.connectSlotsByName(getCustomersHttpDialog)

    def retranslateUi(self, getCustomersHttpDialog):
        _translate = QtCore.QCoreApplication.translate
        getCustomersHttpDialog.setWindowTitle(_translate("getCustomersHttpDialog", "Kunde import fra server"))
        self.buttonStart.setText(_translate("getCustomersHttpDialog", "Start"))
        self.buttonClose.setText(_translate("getCustomersHttpDialog", "Luk"))
