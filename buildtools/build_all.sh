#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

targetdir="../resources"
rm -f ${targetdir}/*_rc.py
./build_icons_rc.sh
./build_ui_rc.sh