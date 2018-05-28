#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Static configuration"""

import os

DEBUG_CALCULATOR = False
DEBUG_CONTACT = False
DEBUG_CUSTOMER = False
DEBUG_EMPLOYEE = False
DEBUG_MAIN = True
DEBUG_PRODUCT = False
DEBUG_REPORT = True
DEBUG_SALELINE = False
DEBUG_SETTINGS = False
DEBUG_VISIT = False
DEBUG_QUERY = False

CONN_CHECK = ["https://wikipedia.org", "https://bitbucket.org", "https://github.com"]
COUNTRIES = [("dk", "Danmark"), ("n", "Norge"), ("s", "Sverige")]
HOME = os.path.expanduser("~")
LOCAL = "{}{}".format(HOME, "./appdata/local/innotec")
APP_DATA = "./appdata"
DBPATH = APP_DATA + "/app.db"
LOGPATH = APP_DATA + "/app.log"
CSV_TABLES = [
    ("Kontakter", "contacts"), ("Kunder", "customers"),
    ("Ordrelinjer", "lines"), ("Rapporter", "reports"),
    ("Ordrer", "visits")
]
HTTP_ENCODING = "ISO-8859-1"
