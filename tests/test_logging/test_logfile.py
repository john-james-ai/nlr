#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_logfile.py                                                                                              #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 12:47:01 pm                                                                        #
# Modified : Monday, November 8th 2021, 12:57:22 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import pytest
import logging
import inspect
from configparser import ConfigParser

from nlr.utils.loggers import LogFile
from nlr.setup import configfile
# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogFileTests:

    def test_get_logfile(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        lf = LogFile()
        logname = 'root'
        level = 'warning'
        key = logname.lower() + '_' + level.lower()
        logfilepath_exp = 'logs/root_warning.log'
        logfilepath_act = lf.get_logfile(logname, level)

        # Confirm correct logfilepath
        config = ConfigParser()
        config.read(configfile)
        assert config['LOGGING'][key], "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = LogFileTests()
    t.test_get_logfile()


# %%
