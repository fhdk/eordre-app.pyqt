#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Passwd Functions"""

import hashlib
import uuid


def hash_password(password):
    """
    Hash a password
    Args:
        password:
    Returns:
        Encoded string
    """
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ":" + salt


def check_password(hashed_password, user_password):
    """
    Check a hashed password
    Args:
        hashed_password:
        user_password:
    Returns:
        bool indicating if a match was found
    """
    password, salt = hashed_password.split(":")
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
