#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_admin.py                                                                                                #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 4:35:35 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 6:27:11 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import pytest
import pandas as pd
import logging
import inspect

from nlr.database.connect import MySQLDatabase, MySQLServer
from nlr.database.admin import Database, Table
from nlr.database import DBNAME
from nlr.database.ddl import TABLES
# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseAdminTests:

    def test_drop(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = Database()
        server_con = MySQLServer()
        with server_con() as connection:
            db.drop(DBNAME, connection)
            assert not db.exists(DBNAME, connection), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create(self):

        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = Database()
        server_conn = MySQLServer()
        with server_conn() as connection:
            db.create(DBNAME, connection, exist_ok=False)
            assert db.exists(DBNAME, connection), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create_exist(self):
        # Should log an error
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = Database()
        server_conn = MySQLServer()
        with server_conn() as connection:
            db.create(DBNAME, connection, exist_ok=False)
            assert db.exists(DBNAME, connection), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create_exist_ok(self):
        # Should log at information level
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = Database()
        server_conn = MySQLServer()
        with server_conn() as connection:
            db.create(DBNAME, connection, exist_ok=True)
            assert db.exists(DBNAME, connection), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


class TableAdminTests:

    TABLE = 'datasources'

    def test_drop(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        table = Table()
        dbconn = MySQLDatabase()
        with dbconn(DBNAME) as connection:
            table.drop(TABLES, connection)
            assert not table.exists(self.TABLE, connection), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        table = Table()
        dbconn = MySQLDatabase()
        with dbconn(DBNAME) as connection:
            table.create(TABLES, connection)
            for name in TABLES.keys():
                assert table.exists(name, connection), "Failure in {}".format(
                    inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create_exist(self):
        # Should log error.
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        table = Table()
        dbconn = MySQLDatabase()
        with dbconn(DBNAME) as connection:
            table.create(TABLES, connection, exist_ok=False)
            for name in TABLES.keys():
                assert table.exists(name, connection), "Failure in {}".format(
                    inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create_exist_ok(self):
        # Should log information
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        table = Table()
        dbconn = MySQLDatabase()
        with dbconn(DBNAME) as connection:
            table.create(TABLES, connection, exist_ok=True)
            for name in TABLES.keys():
                assert table.exists(name, connection), "Failure in {}".format(
                    inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = DatabaseAdminTests()
    t.test_drop()
    t.test_create()
    t.test_create_exist()
    t.test_create_exist_ok()

    t = TableAdminTests()
    t.test_drop()
    t.test_create()
    t.test_create_exist()
    t.test_create_exist_ok()
    # %%
