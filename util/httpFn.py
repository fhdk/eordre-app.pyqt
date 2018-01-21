#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Http functions"""

import ssl
from http.client import HTTPException
from socket import timeout
from urllib.error import URLError
from urllib.request import urlopen, Request

import version

from configuration import config
from . import sanitizeDataFn

USER_AGENT = "Eordre NG version {}".format(version.__version__)

BC = "\033[1;36m"
EC = "\033[0;1m"
DBG = True


def printit(string):
    """
    Print variable string when debugging
    Args:
        string: the string to be printed
    """
    if DBG:
        print("{}\n{}{}{}".format("utils.httpFn.py", BC, string, EC))


def get_customers(settings, employee, maxwait=2):
    """
    Download a file and return content
    Args:
        settings:
        employee:
        maxwait:

    Returns:
        customers list
    """
<<<<<<< HEAD
    active_settings = settings.item_
    active_employee = employee.item_
=======
    active_settings = settings.setting
    active_employee = employee.employee
>>>>>>> version-0.4.1
    try:
        # old file
        # req_file = "".join([active_settings["fc"], active_employee["salesrep"], active_settings["sf"]])
        # new file
        req_file = "".join([active_settings["pf"], active_settings["fc"], active_settings["sf"]])
    except KeyError:
        return

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    data = []
    uri = "{}/{}/{}".format(active_settings["http"], active_settings["usercountry"], req_file)
    printit(" -" + uri)
    request = Request(uri)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urlopen(request, timeout=maxwait, context=context) as response:
            data = response.read()
            try:
                _ = active_employee["salesrep"]
                data = sanitizeDataFn.sanitize_customer_data(data, active_employee["salesrep"])
            except KeyError:
                return data
    except (HTTPException, timeout, URLError) as active_employee:
        print("HTTP ERROR: {}".format(active_employee))

    return data


def get_employee_data(settings, maxwait=2):
    """
    Download a file and return content
    Args:
        settings:
        maxwait:

    Returns:
        current data
    """
<<<<<<< HEAD
    s = settings.item_
=======
    s = settings.setting
>>>>>>> version-0.4.1
    f = "".join([s["pf"], s["fe"], s["sf"]])
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    data = []
    uri = "{}/{}/{}".format(s["http"], s["usercountry"], f)
    request = Request(uri)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urlopen(request, timeout=maxwait, context=context) as response:
            data = response.read()
            data = sanitizeDataFn.sanitize_employee_data(data, s["usermail"], s["userpass"])

    except (HTTPException, timeout, URLError) as e:
        print("HTTP ERROR: {}".format(e))
    return data


def get_modified_date(server, country, file, maxwait=2):
    """
    Download a file and return content

    Args:
        server
        country:
        file:
        maxwait:

    Returns:
        string with date and time
    """
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    uri = "{}/{}/{}".format(server, country, file)
    request = Request(uri)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urlopen(request, timeout=maxwait, context=context) as response:
            data = response.read().decode(config.HTTP_ENCODING)
            return data
    except (HTTPException, timeout, URLError) as e:
        print("HTTP ERROR: {}".format(e))
    return ""


def get_products(settings, maxwait=2):
    """
    Download a file and return content

    Args:
        settings:
        maxwait:

    Returns:
        products list
    """
<<<<<<< HEAD
    s = settings.item_
=======
    s = settings.setting
>>>>>>> version-0.4.1
    f = "".join([s["pf"], s["fp"], s["sf"]])
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    data = []
    uri = "{}/{}/{}".format(s["http"], s["usercountry"], f)
    request = Request(uri)
    request.add_header("User-Agent", USER_AGENT)
    try:
        with urlopen(request, timeout=maxwait, context=context) as response:
            data = response.read()
            data = sanitizeDataFn.sanitize_product_data(data)
    except (HTTPException, timeout, URLError) as e:
        print("HTTP ERROR: {}".format(e))
    return data


def inet_conn_check(maxwait=2):
    """
    Check for internet connection
    Args:
        maxwait:
    Returns:
        bool indicating if internet is available
    """
    data = None
    hosts = config.CONN_CHECK
    for host in hosts:
        # noinspection PyBroadException
        try:
            with urlopen(host, timeout=maxwait) as response:
                data = response.read()
            break
        except (HTTPException, timeout) as e:
            pass
    return bool(data)


def update_last_sync_info(settings):
    """
    Get info about file status
    Args:
        settings:
    Returns:
        Two tuples with target and date time values
    """
<<<<<<< HEAD
    s = settings.item_
=======
    s = settings.setting
>>>>>>> version-0.4.1
    f = "".join([s["pd"], s["fc"], s["sf"]])
    s["sac"] = get_modified_date(s["http"], s["usercountry"], f)
    f = "".join([s["pd"], s["fc"], s["sf"]])
    s["sap"] = get_modified_date(s["http"], s["usercountry"], f)
    return [(s["fc"], s["sac"]), (s["fp"], s["sap"])]
