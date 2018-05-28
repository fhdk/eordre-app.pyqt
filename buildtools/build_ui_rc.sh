#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

builddir=${PWD}
targetdir="../../resources"
cd ./ui
echo "Building Create Report Dialog resource ..."
pyuic5 --from-imports create_report_dialog.ui -o ${targetdir}/create_report_dialog_rc.py
echo "Building Csv File Import Dialog resource ..."
pyuic5 --from-imports csv_file_import_dialog.ui -o ${targetdir}/csv_import_dialog_rc.py
echo "Building Customer Http Dialog resource ..."
pyuic5 --from-imports get_customers_http_dialog.ui -o ${targetdir}/http_customers_dialog_rc.py
echo "Building Product Http Dialog resource ..."
pyuic5 --from-imports get_products_http_dialog.ui -o ${targetdir}/http_products_dialog_rc.py
echo "Building Main Window resource ..."
pyuic5 --from-imports main_window.ui -o ${targetdir}/main_window_rc.py
echo "   Done!"
cd ${builddir}
