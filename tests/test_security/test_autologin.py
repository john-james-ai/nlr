#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_autlogin.py                                                                                             #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Saturday, November 13th 2021, 2:02:24 am                                                                      #
# Modified : Saturday, November 13th 2021, 2:35:47 am                                                                      #
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

from nlr.utils.security import Autologin
# ------------------------------------------------------------------------------------------------------------------------ #

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AutologinTests:

    def test_autologin_exists(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        al = Autologin()

        al.state(name=name)

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_autologin_does_not_exist(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'nlr'
        al = Autologin()

        with pytest.raises(KeyError):
            assert al.state(name=name), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_autologin_on(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        al = Autologin()
        al.on(name)

        assert al.state(name=name), "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_autologin_off(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        name = 'MYSQL_SERVER'
        al = Autologin()
        al.off(name)

        assert not al.state(name=name), "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


def test_autologin():
    logger.info(" Started Autologin Tests")
    t = AutologinTests()
    t.test_autologin_exists()
    t.test_autologin_does_not_exist()
    t.test_autologin_on()
    t.test_autologin_off()
    logger.info(" Completed Autologin Tests. Success!")


if __name__ == "__main__":
    test_autologin()

    # %%
