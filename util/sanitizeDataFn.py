#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Data Sanitize Functions"""

from configuration import config
from util.passwdFn import check_password

__appname__ = "Eordre NG"
__module__ = "sanitizeDataFn"


def sanitize_customer_data(rawdata, sr):
    """
    Sanitizing the raw data from http data file
    Args:
        rawdata:
        sr:
    Returns:
        List of customers filtered by sr
    """
    customer_list = []
    if not rawdata:
        return customer_list
    rawdata = rawdata.replace(bytes("\r\n|", "ascii"), bytes("|", "ascii"))
    customer_data = rawdata.split(bytes("\r\n", "ascii"))
    for data in customer_data:
        if not data:
            continue
        line = data.decode(config.HTTP_ENCODING).split("|")
        if line[6].strip() == sr:
            customer_data = [line[0].strip(), line[1].strip(), line[2].strip(),
                             line[3].strip(), line[4].strip(), line[5].strip(),
                             line[6].strip(), line[7].strip(), line[8].strip(),
                             line[9].strip(), line[10].strip(), line[11].strip()]
            customer_list.append(customer_data)
    return customer_list


def sanitize_employee_data(rawdata, em, hp):
    """
    Sanitizing the raw data from http data file
    Args:
        rawdata:
        em:
        hp:
    Returns:
        current data if passwords match
    """
    emp = []
    if not rawdata:
        return emp
    rawdata = rawdata.replace(bytes("\r\n|", "ascii"), bytes("|", "ascii"))
    employee_data = rawdata.split(bytes("\r\n", "ascii"))
    for data in employee_data:
        if not data:
            continue
        line = data.decode(config.HTTP_ENCODING).split("|")
        if line[2].lower() == em.lower():
            if check_password(hp, line[4]):
                email_lower = line[2].lower()
                country_lower = line[3].lower()
                emp = [line[0].strip(), line[1].strip(), email_lower.strip(),
                       country_lower.strip(), 0]
    return emp


def sanitize_product_data(rawdata):
    """
    Sanitizing the raw data from http data file
    Args:
        rawdata:
    Returns:
        List with products
    """
    product_list = []
    if not rawdata:
        return product_list
    rawdata = rawdata.replace(bytes("\r\n|", "ascii"), bytes("|", "ascii"))
    product_data = rawdata.split(bytes("\r\n", "ascii"))
    for data in product_data:
        if not data:
            continue
        line = data.decode(config.HTTP_ENCODING).split("|")
        product = (line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), line[4].strip(),
                   line[5], line[6], line[7], line[8], line[9], line[10],
                   line[11], line[12], line[13], line[14], line[15], line[16].strip())
        product_list.append(product)
    return product_list
