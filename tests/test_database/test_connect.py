#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_connect.py                                                                                              #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 1:44:19 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 4:57:31 pm                                                                        #
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

from nlr.database.connect import MySQLDatabase, MySQLPool, MySQLServer
from nlr.database import DBNAME
from nlr.utils.security import manual_login, auto_login

# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConnectTests:

    def test_server(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        manual_login()
        server = MySQLServer()

        with server() as connection:
            assert connection.is_connected(), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_database(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = MySQLDatabase()
        with db(DBNAME) as connection:
            assert connection.is_connected(), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_server_autologin(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        auto_login()
        server = MySQLServer()

        with server() as connection:
            assert connection.is_connected(), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_database_autologin(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        db = MySQLDatabase()
        with db(DBNAME) as connection:
            assert connection.is_connected(), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = ConnectTests()
    t.test_server()
    t.test_database()
    t.test_server_autologin()
    t.test_database_autologin()

    # %%
