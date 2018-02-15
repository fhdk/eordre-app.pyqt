#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Contact module"""

from models.query import Query

__module = "contact"


class Contact:
    """
    Contact class
    """

    def __init__(self):
        """Initialize contact class"""
        self.model = {
            "name": "contacts",
            "id": "contact_id",
            "fields": ("contact_id", "customer_id", "name", "department", "email", "phone", "infotext"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "INTEGER NOT NULL", "TEXT", "TEXT", "TEXT", "TEXT", "TEXT")
        }
        self._contact = {}
        self._contacts = []
        self._csv_record_length = 8
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def contact(self):
        """
        Active contact
        :return:
        """
        return self._contact

    @contact.setter
    def contact(self, contact_id):
        """
        Set contact
        :return:
        """
        self.find(contact_id)

    @property
    def list_(self):
        return self._contacts

    @list_.setter
    def list_(self, customer_id):
        self.load_for_customer(customer_id=customer_id)

    @property
    def csv_record_length(self):
        """The number of fields expected on csv import"""
        return self._csv_record_length

    def clear(self):
        """
        Clear internal variables
        """
        self._contact = {}
        self._contacts = []

    def add(self, name, department="", phone="", email="", info=""):
        """
        Create a contact
        Args:
            name:
            department:
            phone:
            email:
            info:
        """
        values = (None, name, department, email, phone, info)
        new_id = self.insert(values)
        return self.find(new_id)

    def delete(self, contact_id):
        """
        Delete contact
        Args:
            contact_id:
        Returns:
            bool
        """
        filters = [("contact_id", "=")]
        values = (contact_id,)
        sql = self.q.build("delete", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return True
        return False

    def find(self, contact_id):
        """
        Load specific contact by id
        Args:
            contact_id:
        Returns:
            bool
        """
        values = (contact_id,)
        sql = self.q.build("select", self.model)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._contact = dict(zip(self.model["fields"], data[0]))
            except IndexError:
                pass
        if success and data:
            return True
        return False

    def translate_row_insert(self, row):
        """
        Translate a csv row
        Args:
            row:
        """
        new_row = (row[0], row[1], row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(), row[7].strip())
        self.insert(new_row)

    def insert(self, values):
        """
        Insert items
        Args:
            values: contact data to insert in contact table
        Returns:
            the new rowid
        """
        sql = self.q.build("insert", self.model)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return False

    def load_for_customer(self, customer_id):
        """
        Load contacts for current
        Args:
            customer_id:
        Returns:
            bool
        """
        filters = [("customer_id", "=")]
        values = (customer_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._contacts = [dict(zip(self.model["fields"], row)) for row in data]
                self._contact = self._contacts[0]
                return True
            except IndexError:
                self._contact = {}
                self._contacts = []
        return False

    def recreate_table(self):
        """
        Drop and create table
        """
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear()

    def update(self):
        """
        Update item
        Returns:
            bool
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._contact.values())
        sql = self.q.build("update", self.model, update=fields, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return True
        return False
