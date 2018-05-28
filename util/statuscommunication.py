#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
"""Communication module"""

from PyQt5.QtCore import QObject, pyqtSignal


class StatusCommunication(QObject):
    """
    Signals for communicating status during imports
    """
    rows_done = pyqtSignal(name="done")  # done signal
    row_count = pyqtSignal(int, name="count")  # row count signal
    row_processing = pyqtSignal(str, name="status")  # status message signal
