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
# Modified : Saturday, November 13th 2021, 3:11:33 pm                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module for creating databases and tables."""
from abc import ABC, abstractmethod
import logging
import mysql.connector
import inspect
import pandas as pd
from mysql.connector import errorcode

from nlr.database.sequel import SEQUEL
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------------------------------ #


class DatabaseAdminBase(ABC):

    def __init__(self):
        self.classname = self.__class__.__name__

    @abstractmethod
    def create(self, name: str, connection: mysql.connector.connect, **kwargs) -> None:
        pass

    @abstractmethod
    def drop(self, name: str, connection: mysql.connector.connect, **kwargs) -> None:
        pass

    @abstractmethod
    def exists(self, name: str, connection: mysql.connector.connect, **kwargs) -> None:
        pass

    @abstractmethod
    def inventory(self, connection: mysql.connector.connect, **kwargs) -> list:
        pass

    def _handle_error(name: str, msg: str, error: mysql.connector.Error) -> None:

        logger.error("Error in {} {} on {}. {}: {}".format(
            self.classname, inspect.stack()[1][3], name, msg, error))
        logger.error("Error Code: ".format(error.errno))
        logger.error("SQL State: ".format(error.sqlstate))
        logger.error("Message: ".format(error.msg))

    def _check_connection(self, connection: mysql.connector.connect) -> None:
        if not connection.is_connected():
            msg = "Connection error in {}:{}. This is supposed to be connected to what??".format(
                self.classname, inspect.stack()[1][3])
            logger.error(msg)
            raise ConnectionError(msg)


class DatabaseAdmin:
    """Create and drop databases."""

    def __init__(self):
        super(DatabaseAdmin, self).__init__()

    def create(self, name: str, connection: mysql.connector.connect, exist_ok=True) -> None:
        """Creates a MySQL database if it does not already exist.

        Arguments:
            name: The name of the database
            connection: A connection to the database server
        """

        self._check_connection(connection)

        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(name))
        except mysql.connector.Error as e:

            if e.errno == errorcode.ER_DB_CREATE_EXISTS:
                msg = "Database {} not created; it already exists.".format(
                    name)
                if exist_ok:
                    logger.info(msg)
                else:
                    self._handle_error(name, msg, e)
            else:
                msg = "Database error"
                self._handle_error(name, msg, e)
        finally:
            cursor.close()

    def drop(self, name: str, connection: mysql.connector.connect) -> None:
        """Drops a MySQL database if it exists.

        Arguments:
            name: The name of the database to drop.
            connection: A connection to the database server.
        """
        self._check_connection(connection)

        cursor = connection.cursor()

        try:
            cursor.execute(
                "DROP DATABASE IF EXISTS {}".format(name))
        except mysql.connector.Error as e:
            msg = "Failed to drop database {}.".format(name)
            self._handle_error(name, msg, e)
        finally:
            cursor.close()

    def inventory(self, connection: mysql.connector.connect) -> list:

        self._check_connection(connection)

        cursor = connection.cursor()
        try:
            cursor.execute("SHOW DATABASES")
            result = cursor.fetchall()
            databases = [row[0] for row in result]
            cursor.close()
            return databases
        except mysql.connector.Error as e:
            msg = "Failed to produce inventory of databases."
            self._handle_error(name, msg, e)
        finally:
            cursor.close()

    def exists(self, name: str, connection: mysql.connector.connect) -> bool:
        """Checks existence of a database by trying to connect to it.

        Arguments:
            name: Name of database
            connection: A MySQL connection to the database server
        """

        self._check_connection(connection)

        databases = self.get_databases(connection)
        exists = True if name in databases else False
        return exists

# ------------------------------------------------------------------------------------------------------------------------ #


class TableAdmin:
    """Create, load, drop and check existence of tables."""

    def __init__(self):
        super(TableAdmin, self).__init__()

    def _create(self, name: str, cursor: mysql.connector.connect().cursor, ddl: dict, exist_ok: bool = True) -> None:

        try:
            cursor.execute(ddl)
            logger.info("Created table {}".format(name))
        except mysql.connector.Error as e:
            if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                msg = "Table {} not created. It already exists.".format(name)
                if exist_ok:
                    logger.info(msg)
                else:
                    self._handle_error(name, msg, e)
            else:
                msg = "Database error. Failed to create table {}".format(name)
                self._handle_error(name, msg, e)

    def create(self, name: str, connection: mysql.connector.connect, ddl: str, exist_ok=True) -> None:
        """Creates a table in the connected database

        Arguments:
            name: The name of the table to create
            connection: The connection to the database in which the table is to be created.
            ddl: The query language to create the table.
            exist_ok: True raises warning if table exists. If False and table exists, an error message is raised

        """
        self._check_connection(connection)

        cursor = connection.cursor()

        self._create(name, cursor, ddl, exist_ok)

        cursor.close()

    def create_tables(self, tables: dict, connection: mysql.connector.connect, exist_ok=True) -> None:
        """Creates one or more tables.

        Arguments:
            tables: A dictionary in which the key corresponds to a table name and the value is the creation SQL.
            connection: A MySQL connection to the database.
        """

        self._check_connection(connection)

        cursor = connection.cursor()

        for name, ddl in tables.items():
            self._create(name, cursor, ddl, exist_ok)

        cursor.close()

    def empty_table(self, name: str, connection: mysql.connector.connect) -> None:
        """Removes all rows from the designated table.

        Arguments:
            name: The name of the table
            connection: A MySQL connection to the database.

        """

        self._check_connection(connection)
        query = "DELETE FROM %s"
        param = (name,)
        try:
            cursor = connection.cursor()
            cursor.execute(query, (table,))
            if self._count_rows(table, connection):
                msg = "Empty table method failed on table {}".format(table)
                logger.error(msg)
                raise Exception(msg)
        except mysql.connector.Error as e:
            msg = "Error in {} {}. Error: {}".format(
                classname, inspect.stack()[0][3], e)
            logger.error(msg)
            raise Exception(msg)
        finally:
            cursor.close()

    def to_tuple(self, data: dict) -> tuple:
        """Converts a dictionary's values to a tuple

        Arguments:
            data: Dictionary who's values must be converted to a single tuple.
        """
        return tuple(v for v in data.values())

    def df_to_tuplelist(self, df: pd.DataFrame) -> list:
        """Converts a DataFrame to a list of tuples that can be loaded into a table.

        Arguments:
            df: The data to be converted
        """
        d = df.to_dict(orient='records')
        tuples = [self.to_tuple(row) for row in d]
        return tuples

    def load(self, table: str, df: pd.DataFrame, connection: mysql.connector.connect) -> None:
        """Loads the table with the data

        Arguments:
            table: The name of the table to be loaded
            df: DataFrame containing the data to load into the table.
            connection: A MySQL connection to the database.

        """

        self._check_connection(connection)

        if self._count_rows(table, connection):
            overwrite = input(
                "The table is not empty. Would you like to overwrite the contents? This is irreversible: [y/n]") or 'n'
            if 'y' in overwrite or 'Y' in overwrite:
                self.empty_table(table, connection)
            else:
                return

        data = self.df_to_tuplelist(df)

        cursor = connection.cursor()

        query = SEQUEL[table]['insert']['sql']

        try:
            cursor.executemany(query, data)
        except mysql.connector.Error as e:
            msg = "Error in {} {}. Error: {}".format(
                classname, inspect.stack()[0][3], e)
            logger.error(msg)
            raise Exception(msg)
        finally:
            cursor.close()

        if not self._count_rows(table, connection):
            msg = "Load {} failed. Zero rows in table.".format(table)
            logger.error(msg)
            raise Exception(msg)

    def drop(self, tables: list, connection: mysql.connector.connect) -> None:
        """Drops a list of tables if they exist

        Arguments:
            tables: List of table names
            connection: A MySQL connection to the database
        """

        self._check_connection(connection)

        cursor = connection.cursor()

        for table in tables:
            try:
                cursor.execute("DROP TABLE IF EXISTS {}".format(table))
                logger.info("Dropped table {}".format(table))
            except mysql.connector.Error as e:
                logger.error(e.msg)
            finally:
                cursor.close()

    def get_tables(self, connection: mysql.connector.connect) -> list:

        if not connection.is_connected():
            logger.error("The connection passed to {} {} is not connected.".format(classname,
                                                                                   inspect.stack()[0][3]))
            raise ConnectionError()

        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        cursor.close()
        tables = []
        if result:
            tables = [row[0] for row in result]

        return tables

    def exists(self, table: str, connection: mysql.connector.connect) -> bool:
        """Checks existence of a table.

        Arguments:
            table: Name of table
            connection: A MySQL connection to the database.
        """

        self._check_connection(connection)

        tables = self.get_tables(connection)
        exists = True if table in tables else False
        return exists

    def _check_connection(self, connection: mysql.connector.connect) -> None:
        if not connection.is_connected():
            logger.error("The connection passed to {} is not connected.".format(
                inspect.stack()[1][3]))
            raise ConnectionError()

    def _count_rows(self, table: str, connection: mysql.connector.connect) -> int:
        """Counts rows in a table.

        Arguments:
            table: The name of the table
            connection: A connection to the database.
        """

        query = """SELECT COUNT(*) from %s"""
        try:
            cursor = connection.cursor()
            cursor.execute(query, (table,))
            count = cursor.fetchall()
            cursor.close()
            return count
        except mysql.connector.Error as e:
            msg = "Error in {} {}. Error: {}".format(
                classname, inspect.stack()[0][3], e)
            logger.error(msg)
            raise Exception(msg)
        finally:
            cursor.close()

        return count
