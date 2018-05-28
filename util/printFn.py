#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

from . import colors as color

DEBUG = 512


def debug(where, what, value):
    """Helper for printing debug messages"""
    print("{} {} >>>> '{} = {}'".format(color.DBG_CLR, where, what, value))


def blue(message):
    """Helper for printing blue messages"""
    print("{}{}{}".format(color.BLUE, message, color.ENDCOLOR))


def green(message):
    """Helper for printing green messages"""
    print("{}{}{}".format(color.GREEN, message, color.ENDCOLOR))


def red(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.RED, message, color.ENDCOLOR))


def yellow(message):
    """Helper for printing yellow messages"""
    print("{}{}{}".format(color.YELLOW, message, color.ENDCOLOR))
