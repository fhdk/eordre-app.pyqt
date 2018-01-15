# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visit_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_visitDialog(object):
    def setupUi(self, visitDialog):
        visitDialog.setObjectName("visitDialog")
        visitDialog.resize(800, 600)
        visitDialog.setMinimumSize(QtCore.QSize(800, 600))

        self.retranslateUi(visitDialog)
        QtCore.QMetaObject.connectSlotsByName(visitDialog)

    def retranslateUi(self, visitDialog):
        _translate = QtCore.QCoreApplication.translate
        visitDialog.setWindowTitle(_translate("visitDialog", "Besøg / Indkøbs ordre"))

