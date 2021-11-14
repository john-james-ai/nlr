#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \connect.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 2:43:46 am                                                                        #
# Modified : Sunday, November 14th 2021, 3:32:50 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
import logging
import mysql.connector
from mysql.connector import errorcode
import contextlib

from nlr.utils.config import Config
from nlr.utils.security import auth
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class MySQLServer:

    @contextlib.contextmanager
    def __call__(self, server: str):
        credentials = auth(server)
        conn = mysql.connector.connect(**credentials)
        try:
            yield conn
        finally:
            conn.close()

    def get_connection(self, server: str) -> mysql.connector.connection:
        credentials = auth(server)
        conn = mysql.connector.connect(**credentials)
        return conn

# ------------------------------------------------------------------------------------------------------------------------ #


class MySQLDatabase:

    @contextlib.contextmanager
    def __call__(self, database: str):
        credentials = auth(database)
        conn = mysql.connector.connect(**credentials)
        try:
            yield conn
        finally:
            conn.close()

    def get_connection(self, database: str) -> mysql.connector.connection:
        credentials = auth(database)
        conn = mysql.connector.connect(**credentials)
        return conn


# ------------------------------------------------------------------------------------------------------------------------ #


class MySQLPool:
    """MySQL database connection pool."""

    __connection_pool = None

    @ staticmethod
    def initialize(name: str, size: int = 5, reset_session: bool = True) -> None:
        """Initializes connection pool

        Arguments:
            name: Name of the database pool
            size: Number of reusable connections in the pool. Default = 5
            reset_session: If True, session variables are reset when connection is returned to the pool.
        """
        credentials = auth(name)

        MySQLPool.__connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=name,
                                                                                  pool_size=size,
                                                                                  **credentials)

        logger.info("Initialized connection pool for {} database.".format(
            dbkey))

    @ staticmethod
    def get_connection():
        conn = MySQLPool.get_connection()
        logger.info(
            "Getting connection from {} connection pool.".format(mysql.connector.name))
        return conn

    @ staticmethod
    def close(connection) -> None:
        logger.info(
            "Returning connection to {} connection pool.".format(connection.name))
        connection.close()
