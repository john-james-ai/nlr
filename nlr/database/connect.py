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
# Modified : Tuesday, November 9th 2021, 1:41:06 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
import logging
import mysql.connector as cnx
from mysql.connector import errorcode

from nlr.utils.config import Config
from nlr.utils.security import auth
from nlr.database import DBNAME, AUTOLOGIN
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class MySQLServer:

    def __call__(self):
        config = Config()
        server = config.read_config('MYSQL', 'server')
        credentials = auth(section=server, resource='server')
        return cnx.connect(**credentials)

# ------------------------------------------------------------------------------------------------------------------------ #


class MySQLDatabase:

    def __call__(self, database: str):
        credentials = auth(section=database, resource='database')
        return cnx.connect(**credentials)

# ------------------------------------------------------------------------------------------------------------------------ #


class MySQLPool:
    """MySQL database connection pool."""

    __connection_pool = None

    @ staticmethod
    def initialize(dbkey: str, name: str, size: int = 5, reset_session: bool = True) -> None:
        """Initializes connection pool

        Arguments:
            dbkey: Database key created at setup
            name: Name of the database pool
            size: Number of reusable connections in the pool. Default = 5
            reset_session: If True, session variables are reset when connection is returned to the pool.
        """

        config = Config()
        credentials = config.read_section(dbkey, as_dict=True)

        MySQLPool.__connection_pool = cnx.pooling.MySQLConnectionPool(pool_name=name,
                                                                      pool_size=size,
                                                                      **credentials)

        logger.info("Initialized connection pool for {} database.".format(
            dbkey))

    @ staticmethod
    def get_connection():
        conn = MySQLPool.get_connection()
        logger.info(
            "Getting connection from {} connection pool.".format(cnx.name))
        return conn

    @ staticmethod
    def close(connection) -> None:
        logger.info(
            "Returning connection to {} connection pool.".format(connection.name))
        connection.close()
