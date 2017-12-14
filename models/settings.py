#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""
settings module
"""

from models.query import Query

__module__ = "settings"


class Settings:
    """
    settings class
    """

    def __init__(self):
        """
        Initialize the settings class
        """
        self.model = {
            "name": "settings",
            "id": "settings_id",
            "fields": ("settings_id", "usermail", "userpass", "usercountry", "pd", "pf", "sf",
                       "http", "smtp", "port", "mailto", "mailserver", "mailport", "mailuser", "mailpass",
                       "fc", "fp", "fe", "lsc", "lsp", "sac", "sap", "sc", "cust_idx", "page_idx", "cust_blob"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT", "INTEGER", "INTEGER", "INTEGER", "BLOB")
        }
        self._settings = {}
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)
            self.get()

    @property
    def item(self):
        """
        current
        Returns:
            The current settings
        """
        try:
            _ = self._settings["usermail"]
        except KeyError:
            self.get()

        return self._settings

    @item.setter
    def item(self, settings):
        """
        Pushing new current settings
        Args:
            settings:
        """
        self._settings = settings
        self.update()

    def get(self):
        """
        Load current
        """
        sql = self.q.build("select", self.model)

        success, data = self.q.execute(sql)

        if success and not data:
            values = (None, "", "", "", "_", "__", ".txt", "", "", "", "", "", "", "", "",
                      "customers", "invenprices", "employees", "", "", "", "", 0, 0, 0, None)

            self.__insert(values)

            success, data = self.q.execute(sql)

        if success and data:
            self._settings = dict(zip(self.model["fields"], data[0]))

        if success and data:
            return data

        return False

    def update(self):
        """
        Update current
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._settings.values())

        sql = self.q.build("update", self.model, update=fields, filters=filters)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            return data

        return False

    def __insert(self, values):
        """
        Inserts in database and activates the current settings values
        Args:
            values:

        Returns:

        """

        sql = self.q.build("insert", self.model)

        success, data = self.q.execute(sql, values=values)

        if success and data:
            self._settings = dict(zip(self.model["fields"], values))
