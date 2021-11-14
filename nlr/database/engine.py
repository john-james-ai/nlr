#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \engine.py                                                                                                    #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Saturday, November 13th 2021, 12:07:15 pm                                                                     #
# Modified : Sunday, November 14th 2021, 5:25:51 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module that executes queries on behalf of database administration and access objects."""
import logging
import mysql.connector
import pandas as pd
from typing import Union, Any
# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------------------------------ #


class DBEngine:
    """Reads, and writes the database on behalf of administration and data access objects."""

    def load(self, query: Query, connection: mysql.connector.connect) -> None:

        try:
            cursor = connection.cursor()
            cursor.executemany(query.query_string, query.parameters)
        except mysql.connector.Error as e:
            handle_error(query=query, error=e)
        finally:
            cursor.close()

    def read(self, query: Query, connection: mysql.connector.connect, as_df: bool = False) -> Union[pd.DataFrame, dict]:
        try:
            cursor = connection.cursor()
            cursor.execute(query.query_string, query.parameters)
            result = cursor.fetchall()
            return result
        except mysql.connector.Error as e:
            handle_error(query=query, error=e)
        finally:
            cursor.close()

    def write(self, query: Query, connection: mysql.connector.connect) -> None:
        try:
            cursor = connection.cursor()
            cursor.execute(query.query_string, query.parameters)
        except mysql.connector.Error as e:
            handle_error(query=query, error=e)
        finally:
            cursor.close()


def handle_error(query: Query, error: mysql.connector.Error = None, is_error: bool = True) -> None:
    if error:
        logger.error(
            "Error in {}:{} while executing {} on {}. Description: {}.  Error: {}".format(
                query.classname, query.methodname, query.name, query.resource, query.description, error
            ))
        logger.error("Error Code: ".format(error.errno))
        logger.error("SQL State: ".format(error.sqlstate))
        logger.error("Message: ".format(error.msg))

    elif is_error:
        logger.error(
            "Error in {}:{} while executing {} on {}. Description: {}.".format(
                query.classname, query.methodname, query.name, query.resource, query.description))
    else:
        logger.info(
            "FYI in {}:{} while executing {} on {}. Description: {}.".format(
                query.classname, query.methodname, query.name, query.resource, query.description))
