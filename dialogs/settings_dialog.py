#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox

from resources.settings_dialog_rc import Ui_settingsDialog
from util import utils, passwdFn


class SettingsDialog(QDialog, Ui_settingsDialog):
    """
    Dialog for entering and updating current
    """

    settings_changed = pyqtSignal()

    def __init__(self, settings, employees, parent=None):
        """Initialize the dialog"""
        super(SettingsDialog, self).__init__(parent)
        self.setupUi(self)  # setup ui from resource file
        self._settings = settings
        self._employees = employees
        self._work = self._settings.item_

        # assign values to input fields
        self.editUserMail.setText(self._settings.item_["usermail"])
        self.editUserPass.setText(self._settings.item_["userpass"])
        self.editUserCountry.setText(self._settings.item_["usercountry"])
        self.editHttp.setText(self._settings.item_["http"])
        self.editSmtp.setText(self._settings.item_["smtp"])
        self.editPort.setText(str(self._settings.item_["port"]))
        self.editMailTo.setText(self._settings.item_["mailto"])
        self.checkServerData.setChecked(utils.int2bool(self._settings.item_["sc"]))
        self.editMailServer.setText(self._settings.item_["mailserver"])
        self.editMailPort.setText(str(self._settings.item_["mailport"]))
        self.editMailUser.setText(self._settings.item_["mailuser"])
        self.editMailPass.setText(self._settings.item_["mailpass"])
        # connect to signals
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self):
        """
        User buttonbox_accepted_action current
        """
        # assign input fields to current
        self._work["usermail"] = self.editUserMail.text().lower()
        self._work["userpass"] = self.editUserPass.text()
        self._work["usercountry"] = self.editUserCountry.text().lower()
        self._work["http"] = self.editHttp.text().lower()
        self._work["smtp"] = self.editSmtp.text().lower()
        self._work["port"] = self.editPort.text()
        self._work["mailto"] = self.editMailTo.text().lower()
        self._work["sc"] = utils.bool2int(self.checkServerData.isChecked())
        self._work["mailserver"] = self.editMailServer.text().lower()
        self._work["mailport"] = self.editMailPort.text()
        self._work["mailuser"] = self.editMailUser.text()
        self._work["mailpass"] = self.editMailPass.text()
        # check validity of important settings
        checkok = True
        items = []
        if self._work["usermail"] == "":
            items.append("Bruger email (fane 1)")
            checkok = False
        if self._work["userpass"] == "":
            items.append("Bruger kode (fane 1)")
            checkok = False
        if self._work["usercountry"] == "":
            items.append("Bruger land (fane 1)")
            checkok = False
        if self._work["smtp"] == "":
            items.append("SMTP server (fane 2)")
            checkok = False
        if self._work["port"] == "":
            items.append("SMTP port (fane 2)")
            checkok = False
        if self._work["mailto"] == "":
            items.append("Ordremodtager (fane 2)")
            checkok = False
        if self._work["http"] == "":
            items.append("Web server (fane 2)")
            checkok = False
        # inform user about settings validity
        if not checkok:
            msgbox = QMessageBox()
            msgbox.warning(self, "Eordre",
                           "Der er mangler i dine indstillinger!\n{}".format("\n".join(items)),
                           QMessageBox.Ok)
            return False
        # update password in settings
        if len(self._work["userpass"]) < 97:
            self._work["userpass"] = passwdFn.hash_password(self._work["userpass"])
        if len(self._work["mailpass"]) < 97:
            self._work["mailpass"] = passwdFn.hash_password(self._work["mailpass"])
        self._settings.report = self._work
        self._settings.update()
        self.settings_changed.emit()
        self.done(True)

    def reject(self):
        """User cancel dialog"""
        self.done(False)
