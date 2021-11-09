#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \security.py                                                                                                  #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 1:15:01 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 2:20:55 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
from getpass import getpass
import logging

from nlr.utils.config import Config
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


def auth(section, resource='database'):
    "Checks user credentials as they are entered and returns True of credentials are correct."

    config = Config()
    auto_login = True if 'True' in config.read_config(
        'MYSQL', 'auto_login') else False

    credentials = config.read_section(section, as_dict=True)

    if auto_login:
        return credentials
    else:
        user_prompt = "Please enter your user id for the {} {}: ".format(
            section, resource)
        pwd_prompt = "Please enter your password for the {} {}: ".format(
            section, resource)
        user = input(user_prompt)
        password = getpass(pwd_prompt)

        if user == credentials['user'] and password == credentials['password']:
            return credentials
        else:
            logger.error(
                "Invalid user id or password for {} {}\n".format(section, resource))
            raise ConnectionError()


def auto_login():
    config = Config()
    config.write_config('MYSQL', 'auto_login', 'True')


def manual_login():
    config = Config()
    config.write_config('MYSQL', 'auto_login', 'False')
