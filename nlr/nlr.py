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
# Modified : Tuesday, November 9th 2021, 1:50:58 am                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Main module."""
from nlr.setup.folders import folder_setup
from nlr.setup.database import database_setup
from nlr.setup.data import data_setup
# %%


def main():
    """Main entry point."""
    config = {}
    print("Welcome to Natural Language Recommendation Project!\nLet's jump right in. We'll need to:\n\t1. Designate your project home and data directories,\n\t2. Setup your MySQL Database\n\t3. Select the data sources that we will be using on the project, and \n\t4. Launch a potentially time-intensive data extraction process. \n\nThis will obviously require us to create directories and download data onto your machine. Our first step is to get your authorization to make such changes to your machine.")

    ok = input(
        "Do we have your authorization to download and organize data on your machine? [y/n]") or 'y'

    if 'y' not in ok:
        print("\n\nNot worries. Please reference the README.md for this project and data setup instructions.")
        exit(0)
    else:
        print("Most excellent. Let's get started.")
        folder_setup()
        # database_setup()
        # data_setup()


if __name__ == "__main__":
    main()
    # %%
