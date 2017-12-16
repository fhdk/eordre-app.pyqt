#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# Copyright: Frede Hundewadt <echo "ZmhAdWV4LmRrCg==" | base64 -d>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

"""Customer products module"""

from models.query import Query
from models.visit import Visit

__module__ = "customer_products"


class CustomerProducts:
    """
    CustomerProduct class
    """

    def __init__(self):
        """
        Initialize CustomerProduct class
        """
        self.model = {
            "name": "customerproducts",
            "id": "cp_id",
            "fields": ("cp_id", "customer_id", "item", "sku", "pcs"),
            "types": ("INTEGER PRIMARY KEY NOT NULL", "INTEGER NOT NULL", "TEXT NOT NULL",
                      "TEXT NOT NULL", "INTEGER DEFAULT 0")
        }
        self._products = []
        self._product = {}
        self.q = Query()
        if not self.q.exist_table(self.model["name"]):
            sql = self.q.build("create", self.model)
            self.q.execute(sql)

    @property
    def list_(self):
        """
        Customer products
        :return:
        """
        return self._products

    @list_.setter
    def list_(self, customer_id):
        """
        Load customers into primary list
        """
        self.__load(customer_id)

    def clear(self):
        """
        Clear internal variables
        """
        self._products = []

    def add(self, customer_id, item, sku, pcs):
        """
        Create a new customer
        Args:
            customer_id:
            item:
            sku:
            pcs:
        Returns:
            bool
        """
        self.insert((None, customer_id, item, sku, pcs))
        self.__load(customer_id)

    def insert(self, values):
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

    def __load(self, customer_id):
        """
        Load products
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
                self._products = [dict(zip(self.model["fields"], row)) for row in data]
                return True
            except IndexError:
                self._products = []
        return False

    def refresh(self, customer_id):
        """
        Refresh customers product list
        Args:
            customer_id
        Returns:
            bool
        """
        visit = Visit()
        selection = ("customer_id",)
        filters = [("customer_id", "=")]
        values = (customer_id,)
        sql = self.q.build("select", visit.model, selection=selection, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success:
            try:
                v_ids = data[0]
                sql = "SELECT lines.sku, sum(pcs) AS pcs, product.item " \
                      "FROM lines " \
                      "INNER JOIN product ON product.sku = lines.sku " \
                      "WHERE cust_id IN ? GROUP BY lines.sku"
                success, data = self.q.execute(sql, v_ids)
                if success:
                    try:
                        self._products = [dict(zip(self.model["fields"], row)) for row in data]
                    except IndexError:
                        pass
                return True
            except IndexError:
                self._products = []
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
        Update customer product list
        Returns:
            bool
        """
        fields = list(self.model["fields"])[1:]
        filters = [(self.model["id"], "=")]
        values = self.q.values_to_update(self._product.values())
        sql = self.q.build("update", self.model, update=fields, filters=filters)
        success, data = self.q.execute(sql, values=values)
        if success and data:
            return True
        return False
