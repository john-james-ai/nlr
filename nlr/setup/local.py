#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \folders.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Sunday, November 7th 2021, 9:12:39 pm                                                                         #
# Modified : Sunday, November 7th 2021, 11:18:45 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import logging
from configparser import ConfigParser
from getpass import getpass
from nlr.setup import configfile
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------ #


class Setup:

    def __init__(self):
        self._config = ConfigParser()
        self._homedir = None
        self._data_home = None
        self._raw_data_home = None
        self._cooked_data_raw = None
        self._model_data = None
        self._configfile = None
        self._db_user = None
        self._db_host = None
        self._db_port = None
        self._db_password = None

    def _store_config(self):
        self._config['PATH'] = {}
        self._config['PATH']['home'] = self._homedir
        self._config['PATH']['data_home'] = self._data_home
        self._config['PATH']['raw_data_home'] = os.path.join(
            self._data_home, 'raw')
        self._config['PATH']['cooked_data_home'] = os.path.join(
            self._data_home, 'cooked')
        self._config['PATH']['model_data_home'] = os.path.join(
            self._data_home, 'model')
        self._config['MYSQL'] = {}
        self._config['MYSQL']['user'] = self._db_user
        self._config['MYSQL']['password'] = self._db_password
        self._config['MYSQL']['host'] = self._db_host
        self._config['MYSQL']['port'] = self._db_port

        with open(configfile, 'w') as fp:
            self._config.write(fp)

    def setup(self):
        """Designates file and folder locations."""
        self._config.read(configfile)
        print(
            "Welcome to Natural Language Recommendation Project! \nLet's jump right in and setup your project and data directories. \nThe project directory defaults to '~/nlr' \nso if you'd like to accept these defaults, simply press enter when prompted. \nReady to go?['y/n']{}.\n\n".format("Y-not"))

        homedir = input(
            "Please enter your project home directory relative to your user home directory.[~/nlr]") or os.path.join("~", "nlr")

        self._homedir = os.path.expanduser(homedir)
        os.makedirs(self._homedir, exist_ok=True)

        data_home = input(
            "Please enter your data home directory  relative to your project home directory, with no leading slashes.['data']") or "data"
        self._data_home = os.path.join(self._homedir, data_home)
        os.makedirs(self._data_home, exist_ok=True)

        self._raw_data_home = os.path.join(self._data_home, "raw")
        os.makedirs(self._raw_data_home, exist_ok=True)

        self._cooked_data_home = os.path.join(self._data_home, "cooked")
        os.makedirs(self._cooked_data_home, exist_ok=True)

        self._model_data_home = os.path.join(self._data_home, "model")
        os.makedirs(self._model_data_home, exist_ok=True)

        db = input(
            "Now we'll move on to the database. If you have not already installed MySQL, please do so and make note of your user, host, port, and password. Shall we proceed with setting the NLR MySQL database? [y/n]") or 'y'

        if 'y' not in db:
            print(
                "That's fine. Simply run 'python nlr database' when you are ready.")
        else:
            self._db_user = input(
                "Great. Please enter your MySQL server user name")
            self._db_host = input(
                "Please enter your host name: ['localhost']") or 'localhost'
            self._db_port = input(
                "Please enter your port number: ['3306']") or '3306'
            self._db_password = getpass(
                "Please enter your MySQL server password")

        print(
            "Ok! We'll setup your database. Now we'll move onto the data.")

        self._store_config()


def main():
    s = Setup()
    s.setup()


if __name__ == "__main__":
    main()

    # %%
