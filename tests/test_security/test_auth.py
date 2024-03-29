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
# Modified : Saturday, November 13th 2021, 2:44:33 am                                                                      #
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

from nlr.utils.security import auth, Autologin
from nlr.database import DBNAME, SERVER

# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthTests:

    def test_auto_login(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        autologin = Autologin()
        autologin.on(name)

        credentials = auth(name=name)
        assert isinstance(credentials, dict), "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_manual_login_success(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        autologin = Autologin()
        autologin.off(name)
        # Success tests
        credentials = auth(name=name)
        assert isinstance(credentials, dict), "Failure in {}".format(
            inspect.stack()[0][3])

    def test_manual_login_failure(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        autologin = Autologin()
        autologin.off(name)
        # Note, enter invalid credentials
        with pytest.raises(ConnectionError):
            assert not auth(name=name), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


def test_auth():
    logger.info(" Started Auth Tests")
    t = AuthTests()
    t.test_auto_login()
    t.test_manual_login_success()
    t.test_manual_login_failure()
    logger.info(" Completed Auth Tests. Success!")


if __name__ == "__main__":
    test_auth()
    # %%
