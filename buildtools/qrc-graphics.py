#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

res_root = "/"
graphic_res_path = os.getenv("PWD")
graphic_dirs = ["splash"]

for graphic_dir in graphic_dirs:
    walk_path = graphic_res_path + "/" + graphic_dir
    f = []
    for (dirpath, dirnames, filenames) in os.walk(walk_path):
        f.extend(filenames)
        break
    outfile = "{}.qrc".format(graphic_dir)
    with open(outfile, "w") as resfile:
        resfile.write("<RCC>\n  <qresource prefix=\"{}\">\n".format(res_root))
        for icon_name in f:
            resfile.write("    <file>{}/{}</file>\n".format(graphic_dir, icon_name))
        resfile.write("  </qresource>\n</RCC>\n")
