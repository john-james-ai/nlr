#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \loggers.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 12:26:37 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 12:32:17 am                                                                       #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #

"""Log Management Utilities."""
import os
from configparser import ConfigParser


# ------------------------------------------------------------------------------------------------------------------------ #


class LogFile:

    def __init__(self):
        self._config = ConfigParser()
        self._config.read(configfile)
        self._logdir = self._config['LOGGING']['logdir']

    def get_logfile(self, logger: str = 'root', level: str = 'debug') -> str:
        """Returns a log filename for the given logger and level."""

        # Standard format for logfile names and paths.
        key = logger.lower() + '_' + level.lower()
        filename = logger.lower() + '_' + level.lower() + '.log'
        filepath = os.path.join(self._logdir, filename)

        # If logfile exists, nothing to do, just return the logfile path.
        self._config.read(configfile)
        if self._config['LOGGING'].get(key, None):
            return filepath

        # Otherwise, add the filename, create the directory if needed, and return the logfile path.
        else:
            self._config['LOGGING'][key] = filepath
            with open(configfile, 'w') as fp:
                self._config.write(fp)
            os.makedirs(filepath, exist_ok=True)
            return filepath
