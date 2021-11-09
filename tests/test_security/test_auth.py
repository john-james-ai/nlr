#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_auth.py                                                                                                 #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 1:56:12 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 2:23:41 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import os
import pytest
import pandas as pd
import logging
import inspect

from nlr.utils.security import auth, auto_login, manual_login
from nlr.database import DBNAME, SERVER

# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthTests:

    def test_auto_login(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        auto_login
        assert auth(section=SERVER, resource='server'), "Failure in {}".format(
            inspect.stack()[0][3])

        assert auth(section=DBNAME, resource='database'), "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_manual_login(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        manual_login()
        # Success tests
        assert auth(section=SERVER, resource='server'), "Failure in {}".format(
            inspect.stack()[0][3])

        assert auth(section=DBNAME, resource='database'), "Failure in {}".format(
            inspect.stack()[0][3])

        # Failure tests
        # Note, enter invalid credentials
        with pytest.raises(ConnectionError):
            assert not auth(section=SERVER, resource='server'), "Failure in {}".format(
                inspect.stack()[0][3])

            assert not auth(section=DBNAME, resource='database'), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = AuthTests()
    t.test_auto_login()
    t.test_manual_login()
    # %%
