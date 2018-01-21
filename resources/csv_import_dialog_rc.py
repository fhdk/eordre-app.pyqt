# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'csv_file_import_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_csvFileImportDialog(object):
    def setupUi(self, csvFileImportDialog):
        csvFileImportDialog.setObjectName("csvFileImportDialog")
        csvFileImportDialog.resize(615, 278)
        csvFileImportDialog.setModal(True)
        self.comboImport = QtWidgets.QComboBox(csvFileImportDialog)
        self.comboImport.setGeometry(QtCore.QRect(140, 10, 210, 40))
        self.comboImport.setObjectName("comboImport")
        self.buttonBrowse = QtWidgets.QPushButton(csvFileImportDialog)
        self.buttonBrowse.setGeometry(QtCore.QRect(370, 10, 229, 40))
        self.buttonBrowse.setAutoDefault(False)
        self.buttonBrowse.setObjectName("buttonBrowse")
        self.buttonImport = QtWidgets.QPushButton(csvFileImportDialog)
        self.buttonImport.setGeometry(QtCore.QRect(370, 50, 229, 40))
        self.buttonImport.setObjectName("buttonImport")
        self.label = QtWidgets.QLabel(csvFileImportDialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 121, 40))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.buttonClose = QtWidgets.QPushButton(csvFileImportDialog)
        self.buttonClose.setGeometry(QtCore.QRect(370, 230, 230, 40))
        self.buttonClose.setObjectName("buttonClose")
        self.txtSelectedFile = QtWidgets.QLineEdit(csvFileImportDialog)
        self.txtSelectedFile.setEnabled(True)
        self.txtSelectedFile.setGeometry(QtCore.QRect(10, 50, 341, 41))
        self.txtSelectedFile.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.txtSelectedFile.setReadOnly(False)
        self.txtSelectedFile.setObjectName("txtSelectedFile")
        self.checkHeaders = QtWidgets.QCheckBox(csvFileImportDialog)
        self.checkHeaders.setGeometry(QtCore.QRect(370, 100, 220, 24))
        self.checkHeaders.setChecked(True)
        self.checkHeaders.setObjectName("checkHeaders")
        self.progressBar = QtWidgets.QProgressBar(csvFileImportDialog)
        self.progressBar.setGeometry(QtCore.QRect(10, 100, 340, 23))
        self.progressBar.setMaximum(1)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setFormat("")
        self.progressBar.setObjectName("progressBar")
        self.log = QtWidgets.QTextBrowser(csvFileImportDialog)
        self.log.setGeometry(QtCore.QRect(10, 130, 340, 140))
        self.log.setObjectName("log")

        self.retranslateUi(csvFileImportDialog)
        QtCore.QMetaObject.connectSlotsByName(csvFileImportDialog)
        csvFileImportDialog.setTabOrder(self.comboImport, self.buttonBrowse)
        csvFileImportDialog.setTabOrder(self.buttonBrowse, self.checkHeaders)
        csvFileImportDialog.setTabOrder(self.checkHeaders, self.buttonImport)
        csvFileImportDialog.setTabOrder(self.buttonImport, self.buttonClose)
        csvFileImportDialog.setTabOrder(self.buttonClose, self.txtSelectedFile)

    def retranslateUi(self, csvFileImportDialog):
        _translate = QtCore.QCoreApplication.translate
        csvFileImportDialog.setWindowTitle(_translate("csvFileImportDialog", "Data import"))
        self.buttonBrowse.setText(_translate("csvFileImportDialog", "Find import fil ..."))
        self.buttonImport.setText(_translate("csvFileImportDialog", "Import"))
        self.label.setText(_translate("csvFileImportDialog", "Import"))
        self.buttonClose.setText(_translate("csvFileImportDialog", "Luk"))
        self.checkHeaders.setText(_translate("csvFileImportDialog", "Første linje er feltnavne"))

