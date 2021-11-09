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
# Modified : Tuesday, November 9th 2021, 1:08:54 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import logging
from getpass import getpass

from nlr.utils.config import Config
from nlr.database.connect import MySQLServer
from nlr.database.create import CreateDatabase, CreateTables
from nlr.database.ddl import TABLES
from nlr.database import DBNAME
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


def setup_database():
    setup_credentials()
    create_database()
    create_tables()


def setup_credentials():

    config = Config()

    print("Let's establish your MySQL server and database credentials.")

    server = input(
        "Please enter a name for your MySQL server (['MYSQL_SERVER']): ") or 'MYSQL_SERVER'
    user = input("Please enter your user id (['root']): ") or 'root'
    password = getpass("Please enter your password: ")
    host = input("Please enter your host ['localhost']: ") or 'localhost'
    port = input("Please enter your port [3306]: ") or '3306'
    database = input("Please enter a database name: ['nlr']: ") or 'nlr'

    print("If you are like me (and I know I am), entering database credentials at connection time can be tedious. If you are working on a local machine we can automatically log you in to the server and database at connection time.")

    auto_login = input(
        "Would you like to auto_login turned on? ['yes', 'no']: ") or 'yes'
    auto_login = 'True' if 'y' in auto_login else 'False'

    # Write MySQL configuration index.
    section = 'MYSQL'
    options = ['server', 'database', 'auto_login']
    values = [server, database, auto_login]
    config.remove_section(section)
    config.write_configs(section, options, values)
    print("\n\nYou have configured the following credentials.")
    config.print_section(section)

    # Write Server Credentials
    section = server
    options = ['user', 'password', 'host', 'port']
    values = [user, password, host, port]
    config.remove_section(section)
    config.write_configs(section, options, values)
    print("\n\nYour server credentials are as follows:")
    config.print_section(section)

    # Write Database Credentials
    section = database
    options = ['user', 'password', 'host', 'port', 'database']
    values = [user, password, host, port, database]
    config.remove_section(section)
    config.write_configs(section, options, values)
    print("\n\nYour database credentials are as follows:")
    config.print_section(section)

    print("Boom! Now we'll create the database and load the datasource metadata")


def create_database():

    # Create the  connection
    db = MySQLServer()
    connection = db(DBNAME)

    # Create the database
    create_db = CreateDatabase()
    create_db(DBNAME, connection)


def create_tables():
    # Create tables
    create_tables = CreateTables()
    create_tables(TABLES, connection)


if __name__ == "__main__":
    setup_database()
# %%
