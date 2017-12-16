#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Customer module"""

from models.query import Query
from util import utils

__module__ = "customer"


class Customer:
    """
    Customer class
    """

    def __init__(self):
        """
        Initialize Customer class
        """
        self.model = {
            "name": "customers",
            "id": "customer_id",
            "fields": ("customer_id", "account", "company",
                       "address1", "address2", "zipcode", "city", "country",
                       "salesrep", "phone1", "vat", "email", "deleted", "modified",
                       "created", "infotext", "att", "phone2", "factor",
                       "body", "plate", "paint", "industry"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "TEXT NOT NULL", "TEXT NOT NULL",
                      "TEXT", "TEXT", "TEXT", "TEXT", "TEXT",
                      "TEXT NOT NULL", "TEXT", "TEXT", "TEXT", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0",
                      "TEXT", "TEXT", "TEXT", "TEXT", "REAL DEFAULT 0",
                      "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0", "INTEGER DEFAULT 0")
        }
        self._customers = []
        self._customer = {}
        self._csv_record_length = 20
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def customer(self):
        """
        Return active customer
        """
        return self._customer

    @customer.setter
    def customer(self, customer_id):
        """
        Set active customer
        Args:
            customer_id
        """
        self.lookup_by_id(customer_id=customer_id)

    @property
    def csv_record_length(self):
        """The number of fields expected on csv import"""
        return self._csv_record_length

    @property
    def list_(self):
        """
        Load customers into primary list
        """
        try:
            _ = self._customers[0]
        except IndexError:
            self._load()
        return self._customers

    def clear_(self):
        """
        Clear internal variables
        """
        self._customer = {}
        self._customers = []

    def add_(self, phone, company, createdate, country, salesrep):
        """
        Create a new customer
        Args:
            phone:
            company:
            createdate:
            country:
            salesrep:
        Returns:
            bool
        """
        found = self.lookup(phone, company)
        if found:
            self._customer = found
            return False
        else:
            values = [None, "NY", company, "", "", "", "", country, salesrep,
                      phone, "", "", 0, 0, createdate, "", "", "", 0.0]
            new_id = self._insert(values)
            self.lookup_by_id(new_id)
        return True

    def update_(self):
        """
        Write self._customer to datafile
        Returns:
            bool
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._customer.values())
        sql = self.q.build("update", self.model, update=fields, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return True
        return False

    def lookup_by_id(self, customer_id):
        """
        Find current by id
        Args:
            customer_id
        Returns:
            bool
        """
        filters = [("customer_id", "=")]
        values = (customer_id,)
        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._customer = dict(zip(self.model["fields"], data[0]))
                return True
            except IndexError:
                self._customer = {}
        return False

    def lookup(self, phone, company, account=None):
        """
        Look up current
        Args:
            account:
            phone:
            company:
        Returns:
            bool
        """
        if account:
            filters = [("account", "=")]
            values = (account,)
        else:
            filters = [("phone1", "=", "and"), ("company", "=")]
            values = (phone, company)

        sql = self.q.build("select", self.model, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if not success:
            filters = [("account", "=", "and"), ("phone1", "="), ("company", "=", "and")]
            values = ("NY", phone, company)
            sql = self.q.build("select", self.model, filters=filters)
            success, data = self.q.execute(sql, values=values)
        if success:
            try:
                self._customer = dict(zip(self.model["fields"], data[0]))
                return True
            except IndexError:
                self._customer = {}
        return False

    def recreate_table(self):
        """
        Drop and create table
        """
        sql = self.q.build("drop", self.model)
        self.q.execute(sql)
        sql = self.q.build("create", self.model)
        self.q.execute(sql)
        self.clear_()

    def translate_row_insert(self, row):
        """
        Translate a csv row
        Args:
            row:
                The expected file format contains data in the following sequence
                id acc comp add1 add2 zipcode city country s_rep phon1 vat email del mod cre info
        """
        # translate field from bool text to integer
        field_15 = utils.bool2int(utils.arg2bool(row[15]))
        # strip trailing spaces from from text fields
        new_row = (row[0],
                   row[1].strip(), row[2].strip(), row[3].strip(), row[4].strip(), row[5].strip(),
                   row[6].strip(), row[7].strip(), row[8].strip(), row[9].strip(), row[10].strip(),
                   row[12].strip(), field_15, row[16], row[17],
                   row[19].strip(), "", "", 0.0, 0, 0, 0, 0)
        self._insert(new_row)

    def import_http(self, values):
        """
        Import customers from http
        Args:
            values: List with values from http request
            expected incoming fields: acc comp add1 add2 zipcity country s_rep phone1 vat email att phon2
        """
        # import file has 'zip  city'
        # app use 'zip' 'city' in different columns
        # zip city can contain more than one space
        # eg '2200  København K' or '4430 Kirke Hyllinge'
        # get the first occurence of space
        # and insert '|' and use it to split zip and city
        loc = values[4].get(" ")
        zipcity = values[4][:loc] + "|" + values[4][loc:]
        zipcity = zipcity.split("|")
        zipcode = zipcity[0].strip()
        city = zipcity[1].strip()
        phone = values[7].strip()
        account = values[0].strip()
        company = values[1].strip()
        # lookup existing current
        if self.lookup(values[7], values[1], values[0]):
            # sanitize and assign values
            if self._customer["account"] == 'NY':
                self._customer["account"] = account
            if self._customer["modified"] == 1:
                self._customer["modified"] = 0
            self._customer["company"] = company
            self._customer["address1"] = values[2].strip()
            self._customer["address2"] = values[3].strip()
            self._customer["zipcode"] = zipcode  # zipcity[4]
            self._customer["city"] = city  # zipcity[4]
            # skip over country[5] and salesrep[6]
            self._customer["phone1"] = phone
            self._customer["vat"] = values[8].strip()
            self._customer["email"] = values[9].strip()
            self._customer["att"] = values[10].strip()
            self._customer["phone2"] = values[11].strip()
            self.update_()  # call update function
        else:
            row_values = (None, account, company, values[2], values[3].strip(), zipcode, city,
                          values[5].strip(), values[6].strip(), phone, values[8].strip(),
                          values[9].strip(), 0, 0, 0, "", values[10].strip(), values[11].strip(), 0.0, 0, 0, 0, 0)
            self._insert(row_values)

    def _insert(self, values):
        """
        Insert a new current
        Args:
            values:
        Returns:
            rowid
        """
        sql = self.q.build("insert", self.model)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return data
        return False

    def _load(self):
        """
        Load customers
        Returns:
            bool
        """
        sql = self.q.build("select", self.model)
        success, data = self.q.execute(sql)
        if success:
            try:
                self._customers = [dict(zip(self.model["fields"], row)) for row in data]
                self._customer = self._customers[0]
                return True
            except IndexError:
                self._customer = {}
                self._customers = []
        return False
