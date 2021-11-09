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
# Modified : Tuesday, November 9th 2021, 2:23:03 am                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import logging
import pandas as pd

from nlr.utils.config import Config
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------ #


def folder_setup():
    """Setup a few folders under the designated home project directory."""
    config = Config()

    # Get expanded default project home directory based upon environment
    default_home = os.getcwd() if 'dev' in config.read_config(
        'SETUP', 'env') else os.path.join("~", "nlr")
    default_home = os.path.expanduser(default_home)

    # Format the keys / options
    options = ['home', 'data_home', 'raw', 'cooked']

    # Format the values / directories
    home = os.path.expanduser(input(
        "Please enter your project home directory relative to your user home directory.[{}]".format(default_home)) or default_home)
    data_home = os.path.expanduser(os.path.join(home, 'data'))
    raw = os.path.expanduser(os.path.join(data_home, 'raw'))
    cooked = os.path.expanduser(os.path.join(data_home, 'cooked'))

    values = [home, data_home, raw, cooked]

    # Indicate whether the paths already existed
    actions = [not os.path.exists(v) for v in values]

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


if __name__ == "__main__":
    folder_setup()

    # %%
