#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Create Report Dialog"""
import datetime

from PyQt5.QtWidgets import QDialog, QMessageBox

from resources.create_report_dialog_rc import Ui_createReportDialog


class ReportDialogCreate(QDialog, Ui_createReportDialog):
    """
    Create a new reportid for date
    """

    def __init__(self, workdate, parent=None):
        """Initialize Dialog"""
        super(ReportDialogCreate, self).__init__(parent)
        self.setupUi(self)
        self.workdate = workdate  # assign date
        self.lineEdit.setText(workdate)  # set workdate in lineedit
        # connect to signals
        self.buttonBox.accepted.connect(self.buttonbox_accepted_action)
        self.buttonBox.rejected.connect(self.buttonbox_rejected_action)

    def buttonbox_accepted_action(self):
        """Slot for buttonbox accepted signal"""
        try:
            # validate if it is ISO format
            datetime.datetime.strptime(self.lineEdit.text(), '%Y-%m-%d')
            self.workdate = self.lineEdit.text()
            self.done(True)
        except ValueError:
            msgbox = QMessageBox
            msgbox.warning(self,
                           "Eordre",
                           "Dato er forkert, det skal være en gyldig dato<br/><strong>Tip:</strong>ÅÅÅÅ-MM-DD!",
                           QMessageBox.Ok)
            return False

    def buttonbox_rejected_action(self):
        """Slot for buttonbox rejected signal"""
        self.done(False)
