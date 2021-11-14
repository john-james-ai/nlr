#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \config.py                                                                                                    #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 11:25:50 pm                                                                        #
# Modified : Saturday, November 13th 2021, 6:53:41 am                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
import os
from configparser import ConfigParser
import pandas as pd
# ------------------------------------------------------------------------------------------------------------------------ #
configfile = os.path.join("config", "config.ini")
# ------------------------------------------------------------------------------------------------------------------------ #


class Config:

    def exists(self, name: str) -> bool:
        """Returns True if the named section exists, False otherwise.

        Arguments:
            name : The name of the resource
        """

        config = ConfigParser()
        config.read(configfile)
        return name in config.sections()

    def read_config(self, section: str, option: str):
        config = ConfigParser()
        config.read(configfile)
        return config[section][option]

    def read_section(self, section: str, as_df=False):
        """Returns the a section configuration.

        Arguments:
            section: The section of the configuration to read
            as_dict: If True return as dictionary, otherwise return as dataframe.
        """
        config = ConfigParser()
        config.read(configfile)
        options = config[section]
        d = {}
        for option in options:
            d[option] = self.read_config(section, option)

        if as_df:
            return pd.DataFrame.from_dict(d, orient='index')

        else:
            return d

    def write_config(self, section: str, option: str, value: str):
        config = ConfigParser()
        config.read(configfile)
        try:
            config[section][option] = value
        except KeyError as e:
            config[section] = {}
            config[section][option] = value
        with open(configfile, 'w') as fp:
            config.write(fp)

    def write_configs(self, section: str, options: list, values: list):
        assert len(options) == len(
            values), "Error in Config.write_configs: options and values lists must have same length."
        for i in range(len(options)):
            self.write_config(section, options[i], values[i])

    def write_options(self, section: str, options: list):
        """Options are expected to be a list of key/value pairs."""
        config = ConfigParser()
        config.read(configfile)
        for option in options:
            for k, v in option.items():
                self.write_config(section=section, option=k, value=v)

    def remove_section(self, section: str):
        config = ConfigParser()
        config.read(configfile)
        config.remove_section(section)
        with open(configfile, 'w') as fp:
            config.write(fp)

    def remove_option(self, section: str, option: str):
        config = ConfigParser()
        config.read(configfile)
        config.remove_option(section, option)
        with open(configfile, 'w') as fp:
            config.write(fp)

    def print_section(self, section: str):
        config = ConfigParser()
        config.read(configfile)
        d = self.read_section(section, as_df=False)
        try:
            d['password'] = '*****'
        except KeyError() as e:
            pass
        df = pd.DataFrame.from_dict(d, orient='index')
        print("\n\n")
        print("{}".format(section))
        print(df.to_string())
        print("\n")
