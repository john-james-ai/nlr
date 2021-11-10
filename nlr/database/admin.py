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
# Modified : Tuesday, November 9th 2021, 7:12:26 pm                                                                        #
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


class Database:
    """Create and drop databases."""

    def create(self, dbname: str, connection: cnx.connect, exist_ok=True) -> None:
        """Creates a MySQL database if it does not already exist.

        Arguments:
            dbname: The name of the database
            connection: A connection to the database server
        """
        cursor = connection.cursor()
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(dbname))
        except cnx.Error as e:

            if e.errno == errorcode.ER_DB_CREATE_EXISTS:
                if exist_ok:
                    logger.info(
                        "Database {} not created; it already exists.".format(dbname))
                else:
                    logger.error(
                        "Database {} not created; it already exists.".format(dbname))
            else:
                logger.error(
                    "Failed to create database: {}. Error: ".format(dbname, e))
                logger.error("Error Code: ".format(e.errno))
                logger.error("SQL State: ".format(e.sqlstate))
                logger.error("Message: ".format(e.msg))
        finally:
            cursor.close()

    def drop(self, dbname: str, connection: cnx.connect) -> None:
        """Drops a MySQL database if it exists.

        Arguments:
            dbname: The name of the database to drop.
            connection: A connection to the database server.
        """
        cursor = connection.cursor()
        try:
            cursor.execute(
                "DROP DATABASE IF EXISTS {}".format(dbname))
        except cnx.Error as e:
            logger.warn(
                "Failed to drop database: {}. Error: ".format(dbname, e))
        finally:
            cursor.close()

    def get_databases(self, connection: cnx.connect) -> list:

        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES")
        result = cursor.fetchall()
        cursor.close()
        if result:
            databases = [row[0] for row in result]

        return databases

    def exists(self, dbname: str, connection: cnx.connect) -> bool:
        """Checks existence of a database by trying to connect to it.

        Arguments:
            dbname: Name of database
            connection: A MySQL connection to the database server
        """
        databases = self.get_databases(connection)
        exists = True if dbname in databases else False
        return exists

        # ------------------------------------------------------------------------------------------------------------------------ #


class Table:
    """Create drop and check existence of tables."""

    def create(self, tables: dict, connection: cnx.connect, exist_ok=True) -> None:
        """Creates one or more tables.

        Arguments:
            tables: A dictionary in which the key corresponds to a table name and the value is the creation SQL.
            connection: A MySQL connection to the database.
        """

        cursor = connection.cursor()

        for name, ddl in tables.items():
            try:
                cursor.execute(ddl)
                logger.info("Created table {}".format(name))
            except cnx.Error as e:
                cursor.close()
                if e.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    if exist_ok:
                        logger.info(
                            "Table {} not created. It already exists.".format(name))
                    else:
                        logger.error(
                            "Table {} not created. It already exists.".format(name))
                else:
                    logger.error(
                        "Failed to create table: {}. Error: ".format(namme, e))
                    logger.error("Error Code: ".format(e.errno))
                    logger.error("SQL State: ".format(e.sqlstate))
                    logger.error("Message: ".format(e.msg))
            else:
                print("Ok")
        cursor.close()

    def drop(self, tables: list, connection: cnx.connect) -> None:
        """Drops a list of tables if they exist

        Arguments:
            tables: List of table names
            connection: A MySQL connection to the database
        """

        cursor = connection.cursor()

        for table in tables:
            try:
                cursor.execute("DROP TABLE IF EXISTS {}".format(table))
                logger.info("Dropped table {}".format(table))
            except cnx.Error as e:
                logger.error(e.msg)
                cursor.close()
        cursor.close()

    def get_tables(self, connection: cnx.connect) -> list:
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        cursor.close()
        tables = []
        if result:
            tables = [row[0] for row in result]

        return tables

    def exists(self, table: str, connection: cnx.connect) -> bool:
        """Checks existence of a table.

        Arguments:
            table: Name of table
            connection: A MySQL connection to the database.
        """
        tables = self.get_tables(connection)
        exists = True if table in tables else False
        return exists
