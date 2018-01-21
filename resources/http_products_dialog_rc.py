# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'get_products_http_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_getProductsHttpDialog(object):
    def setupUi(self, getProductsHttpDialog):
        getProductsHttpDialog.setObjectName("getProductsHttpDialog")
        getProductsHttpDialog.resize(540, 120)
        self.progressBar = QtWidgets.QProgressBar(getProductsHttpDialog)
        self.progressBar.setGeometry(QtCore.QRect(370, 80, 160, 23))
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.buttonStart = QtWidgets.QPushButton(getProductsHttpDialog)
        self.buttonStart.setGeometry(QtCore.QRect(370, 10, 161, 26))
        self.buttonStart.setObjectName("buttonStart")
        self.buttonClose = QtWidgets.QPushButton(getProductsHttpDialog)
        self.buttonClose.setGeometry(QtCore.QRect(370, 40, 161, 26))
        self.buttonClose.setObjectName("buttonClose")
        self.log = QtWidgets.QTextBrowser(getProductsHttpDialog)
        self.log.setGeometry(QtCore.QRect(10, 10, 340, 100))
        self.log.setObjectName("log")

        self.retranslateUi(getProductsHttpDialog)
        QtCore.QMetaObject.connectSlotsByName(getProductsHttpDialog)

    def retranslateUi(self, getProductsHttpDialog):
        _translate = QtCore.QCoreApplication.translate
        getProductsHttpDialog.setWindowTitle(_translate("getProductsHttpDialog", "Prisliste import fra server"))
        self.buttonStart.setText(_translate("getProductsHttpDialog", "Start"))
        self.buttonClose.setText(_translate("getProductsHttpDialog", "Luk"))

