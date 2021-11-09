#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \create.py                                                                                                    #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 8:59:27 pm                                                                         #
# Modified : Tuesday, November 9th 2021, 5:02:38 am                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module for creating databases and tables."""
import logging
import mysql.connector as cnx
from mysql.connector import errorcode
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------------------------------ #


class CreateDatabase:

    def __call__(self, dbname: str, connection: cnx.connect):
        cursor = connection.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname))
        except cnx.Error as e:
            logger.warn("Failed to create database: {}".format(e))


# ------------------------------------------------------------------------------------------------------------------------ #


class CreateTables:
    """Creates tables from a dictionary of ddl.

    Arguments:
        tables: dictionary of table creation ddl, keyed by each tablename
    """

    def __call__(self, tables: dict, connection: cnx.connect):

        cursor = connection.cursor()

        for name, ddl in tables.items():
            try:
                print("Creating table {}: ".format(name), end='')
                cursor.execute(ddl)
            except cnx.Error as e:
                if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(e.msg)
            else:
                print("Ok")

        cursor.close()
        cnx.close()
