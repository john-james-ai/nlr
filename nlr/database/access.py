#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \queries.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 8:24:49 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 10:37:17 pm                                                                       #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
from abc import ABC, abstractmethod
import logging
import mysql.connector as cnx
from typing import Any
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class DBAccess:
    """Provides access to the underlying databases."""

    def modify(self, query: Query, connection: cnx.connection) -> None:
        cursor = connection.cursor()
        try:
            cursor.execute(query.sql, query, params)
            cursor.close
            logger.info("Executed {}".format(query.description))
        except cnx.Error as e:
            msg = "Error occurred in query {} while inserting into the {} table. Error: {}".format(
                query.name, query.table, e)
            logger.error(msg)
            raise
        finally:
            cursor.close()

    def read(self, query: Query, connection: cnx.connection) -> Query:
        cursor = connection.cursor()
        try:
            cursor.execute(query.sql, query, params)
            query.results = cursor.fetchall()
            cursor.close
            logger.info("Executed {}".format(query.description))
        except cnx.Error as e:
            msg = "Error occurred in query {} while reading from {} table. Error: {}".format(
                query.name, query.table, e)
            logger.error(msg)
            raise
        finally:
            cursor.close()

        return query


class Query:
    """Standard Query object encapsulating the parameterized SQL string, and parameters.

    Arguments:
        name: Name for the query. Defaults to the classname of the Query factory.
        description: Short sentence summary used for logging.
        table: Name of table upon which the query is executed
        qtype: One of ['insert', 'select', 'update', 'delete']
        sql: Parameterized query string.
        params: Tuple containing query parameters
        result: Results of the query.

    """

    def __init__(self, name: str, table: str, qtype: str, sql: str, params: tuple):
        self.name = name
        self.description = description
        self.table = table
        self.qtype = qtype
        self.sql = sql
        self.params = params
        self.results = None
