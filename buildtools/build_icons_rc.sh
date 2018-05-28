#!/bin/bash
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# init
builddir=${PWD}
targetdir="../../resources"

# building icons
cd ${builddir}/icons
# build qrc file
python ${builddir}/qrc-icons.py
# build resource file
echo "Building system icon resource ..."
pyrcc5 system.qrc -o ${targetdir}/system_rc.py

# building graphics
cd ${builddir}/graphics
# build qrc file
python ${builddir}/qrc-graphics.py
# build resource file
echo "Building splash resource ..."
pyrcc5 splash.qrc -o ${targetdir}/splash_rc.py

# done
echo "   Done!"
cd ${builddir}

