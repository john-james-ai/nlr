#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \database.py                                                                                                  #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 11:09:34 pm                                                                        #
# Modified : Saturday, November 13th 2021, 9:24:48 am                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import logging
from getpass import getpass
import time
import pandas as pd

from nlr.utils.config import Config
from nlr.database.connect import MySQLServer, MySQLDatabase
from nlr.database.admin import DatabaseAdmin, TableAdmin
from nlr.database import SERVER, DBNAME, PORT, HOST
from nlr.database.sequel import TABLES

# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


def setup_database(server: str, database: str, host: str, port: str, table_ddl: dict):
    setup_credentials(server, database, host, port)
    create_database(server, database)
    create_tables(database, table_ddl)
    df = get_datasources()
    load_table(database, table_name='datasource', data=df)


def get_datasources() -> pd.DataFrame:
    config = Config()
    filepath = config.read_config('DATASOURCE', 'filepath')
    df = pd.read_csv(filepath)
    return df


def load_table(database: str, table_name: str, data: pd.DataFrame) -> None:

    table_admin = TableAdmin()
    conn = MySQLDatabase()
    with conn(database) as connection:
        table_admin.load(table_name, data, connection)


def _setup_credentials(server: str, database: str, host: str, port: str) -> None:

    config = Config()

    user = input("Please enter your user id (['root']): ") or 'root'
    password = getpass("Please enter your password: ")
    autologin = input(
        "Would you like to enable autologin? [y/n]: ") or 'y'
    autologin = True if 'y' in autologin else False

    # Write MySQL configuration index.
    section = server
    options = ['user', 'password', 'host', 'port']
    values = [user, password, host, port]
    config.remove_section(section)
    config.write_configs(section, options, values)
    print("\nYour database server credentials are as follows:")
    config.print_section(section)

    # Write Database Credentials
    time.sleep(1)
    section = database
    options = ['user', 'password', 'host', 'port', 'database']
    values = [user, password, host, port, database]
    config.remove_section(section)
    config.write_configs(section, options, values)
    print("\nYour database credentials are as follows:")
    config.print_section(section)

    # Write Autologin Credentials
    time.sleep(1)
    section = 'AUTOLOGIN'
    options = [server, database]
    values = [str(autologin), str(autologin)]
    config.write_configs(section, options, values)


def setup_credentials(server: str, database: str, host: str, port: str) -> None:

    print("\n\nLet's establish your MySQL server and database credentials.")
    time.sleep(1)
    _setup_credentials(server, database, host, port)

    print("Boom! Now we'll create the database and load the datasource metadata")


def create_database(server: str, database: str) -> None:
    """Creates the database

    Arguments:
        server: The name of the database server
        database: The name of the database to create

    """

    conn = MySQLServer()
    with conn(server) as connection:
        db = DatabaseAdmin()
        db.create(database, connection)


def create_tables(database: str, table_ddl) -> None:
    """Creates the tables in the designated database

    Arguments:
        database: The existing database into which the tables will be created.
        tables: The dictionary  containing the table creating ddl
    """

    conn = MySQLDatabase()
    table_admin = TableAdmin()
    with conn(database) as connection:
        table_admin.create(table_ddl, connection)
        for table_name in table_ddl.keys():
            assert table_admin.exists(table_name, connection), logger.error(
                "Error creating {}. Did not pass existence check.".format(table_name))


if __name__ == "__main__":
    setup_database(SERVER, DBNAME, HOST, PORT, TABLES)
# %%
