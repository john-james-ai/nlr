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
# Modified : Saturday, November 13th 2021, 6:28:52 am                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import time
import logging
import pandas as pd

from nlr.utils.config import Config
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------ #


def _setup_folders():
    """Setup a few folders under the designated home project directory."""
    config = Config()

    # Format the keys / options
    options = ['home', 'data_home', 'raw', 'interim', 'processed', 'cooked']

    # Format the values / directories
    home = input(
        "Please enter the name of your project home directory") or 'nlr'
    time.sleep(1)
    home = os.path.expanduser(os.path.join('~', home))
    data_home = os.path.join(home, 'data')
    raw = os.path.join(data_home, 'raw')
    interim = os.path.join(data_home, 'interim')
    processed = os.path.join(data_home, 'processed')
    cooked = os.path.join(data_home, 'cooked')

    values = [home, data_home, raw, interim, processed, cooked]

    # Indicate whether the paths already existed
    actions = []
    for v in values:
        actions.append("Created" if not os.path.exists(v)
                       else "Already Exists")

    # Create the directories if they don't already exist
    [os.makedirs(v, exist_ok=True) for v in values]

    # Format the data for printing
    print("The following summaries the folders created or existed.")
    d = {}
    d['Keys'] = options
    d['Folders'] = values
    d['Created'] = actions

    df = pd.DataFrame(data=d)
    print(df.to_string(index=False))

    options_list_of_dictionaries = []
    # Combine the lists, create the directories and update the config file.
    for k, v in zip(options, values):
        d = {}
        d[k] = v
        options_list_of_dictionaries.append(d)

    config.write_options('PATH', options_list_of_dictionaries)


def setup_folders():
    # Setup folders only if not in development.
    config = Config()
    env = config.read_config('ENVIRONMENT', 'dev')
    if 'F' in env or 'f' in env or not env:
        _setup_folders()
    else:
        print("\nDevelopment environment has already been setup.\n\n")


if __name__ == "__main__":
    setup_folders()

    # %%
