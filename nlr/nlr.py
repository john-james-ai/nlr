#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \nlr.py                                                                                                       #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Sunday, November 7th 2021, 11:25:53 pm                                                                        #
# Modified : Saturday, November 13th 2021, 8:31:25 am                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Main module."""
import time
from nlr.setup.folders import setup_folders
from nlr.setup.database import setup_database
from nlr.database.sequel import TABLES
from nlr.database import DBNAME, SERVER, HOST, PORT
# %%


def authorize():

    ok = input(
        "Do we have your authorization to download and organize data on your machine? [y/n]") or 'y'

    if 'y' in ok or 'Y' in ok:
        print("Most excellent. Let's get started.\n\n")
        time.sleep(1)
        return True

    else:
        print("Not worries. Please reference the README.md for this project and data setup instructions.\n\n")
        time.sleep(1)
        return False


def main():
    """Main entry point."""
    config = {}
    print("Welcome to Natural Language Recommendation Project!\nLet's jump right in. We'll need to:\n\t1. Designate your project home and data directories,\n\t2. Setup your MySQL Database\n\t3. Select the data sources that we will be using on the project, and \n\t4. Launch a potentially time-intensive data extraction process. \n\n")

    time.sleep(1)

    print("This will obviously require us to create directories and download data onto your machine.")

    time.sleep(1)

    if authorize():
        setup_folders()
        time.sleep(1)
        setup_database(SERVER, DBNAME, HOST, PORT, TABLES)


if __name__ == "__main__":
    main()
    # %%
