# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_customers_http_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_getCustomersHttpDialog(object):
    def setupUi(self, getCustomersHttpDialog):
        getCustomersHttpDialog.setObjectName("getCustomersHttpDialog")
        getCustomersHttpDialog.resize(540, 120)
        self.progressBar = QtWidgets.QProgressBar(getCustomersHttpDialog)
        self.progressBar.setGeometry(QtCore.QRect(370, 80, 160, 23))
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.buttonStart = QtWidgets.QPushButton(getCustomersHttpDialog)
        self.buttonStart.setGeometry(QtCore.QRect(370, 10, 161, 26))
        self.buttonStart.setObjectName("buttonStart")
        self.buttonClose = QtWidgets.QPushButton(getCustomersHttpDialog)
        self.buttonClose.setGeometry(QtCore.QRect(370, 40, 161, 26))
        self.buttonClose.setObjectName("buttonClose")
        self.log = QtWidgets.QTextBrowser(getCustomersHttpDialog)
        self.log.setGeometry(QtCore.QRect(10, 10, 340, 100))
        self.log.setObjectName("log")

        self.retranslateUi(getCustomersHttpDialog)
        QtCore.QMetaObject.connectSlotsByName(getCustomersHttpDialog)

    def retranslateUi(self, getCustomersHttpDialog):
        _translate = QtCore.QCoreApplication.translate
        getCustomersHttpDialog.setWindowTitle(_translate("getCustomersHttpDialog", "Kunde import fra server"))
        self.buttonStart.setText(_translate("getCustomersHttpDialog", "Start"))
        self.buttonClose.setText(_translate("getCustomersHttpDialog", "Luk"))

