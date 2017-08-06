#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <f@hundewadt.dk>
# Copyright: Frede Hundewadt <fh@uex.dk>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
Settings module
"""

from configuration import config
from models.query import Query


class Settings:
    """
    Settings class
    """
    def __init__(self):
        """
        Initialize the Settings class
        """
        self.model = {
            "name": "settings",
            "id": "settingsid",
            "fields": ("settingsid", "usermail", "userpass", "usercountry", "pd", "pf", "sf",
                       "http", "smtp", "port", "mailto", "mailserver", "mailport", "mailuser", "mailpass",
                       "fc", "fp", "fe", "lsc", "lsp", "sac", "sap", "sc"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER")
        }
        self._settings = {}
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            success, data = self.q.execute(sql)
            if config.DEBUG_SETTINGS:
                print("\033[0;33m{}\n ->table\n  ->success: {}\n  ->data: {}\033[0;1m".format(
                    self.model["name"], success, data))

    @property
    def settings(self):
        """
        Settings
        Returns:
            The settings
        """
        try:
            _ = self._settings["usermail"]
        except KeyError:
            self.load()

        return self._settings

    @settings.setter
    def settings(self, settings):
        """
        Pushing new settings
        Args:
            settings:
        """
        self._settings = settings
        self.update()

    def insert(self, values):
        """
        Inserts in database and activates the settings values
        Args:
            values:

        Returns:

        """

        sql = self.q.build("insert", self.model)

        if config.DEBUG_SETTINGS:
            print("\033[0;33m{}\n ->insert\n  ->sql: {}\n  ->values: {}".format(
                self.model["name"], sql, values))

        success, data = self.q.execute(sql, values=values)

        if config.DEBUG_SETTINGS:
            print("  ->success: {}\n  ->data: {}\033[0;1m".format(success, data))

        if success and data:
            self._settings = dict(zip(self.model["fields"], values))

    def load(self):
        """
        Load settings
        """
        # build query and execute
        sql = self.q.build("select", self.model)

        if config.DEBUG_SETTINGS:
            print("\033[0;33m{}\n ->load\n  ->sql: {}".format(self.model["name"], sql))

        success, data = self.q.execute(sql)

        if success and not data:
            values = (None, "", "", "", "_", "__", ".txt", "", "", "", "", "", "", "", "",
                      "customers", "invenprices", "employees", "", "", "", "", 0)

            self.insert(values)

            success, data = self.q.execute(sql)

        if success and data:
            self._settings = dict(zip(self.model["fields"], data[0]))

        if config.DEBUG_SETTINGS:
            print("  ->success: {}\n  ->data: {}\033[0;1m".format(success, data))

        if success and data:
            return data

        return False

    def update(self):
        """
        Update settings
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_arg(self._settings.values())

        sql = self.q.build("update", self.model, update=fields, filteron=filters)

        if config.DEBUG_SETTINGS:
            print("\033[0;33m{}\n ->update\n  ->fields: {}\n  ->filters: {}\n  ->values: {}\n  ->sql: {}".format(
                self.model["name"], fields, filters, values, sql))

        success, data = self.q.execute(sql, values=values)

        if config.DEBUG_SETTINGS:
            print("  ->success: {}\ndata: {}\033[0;1m".format(success, data))

        if success and data:
            return data

        return False
