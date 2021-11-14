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
# Modified : Saturday, November 13th 2021, 6:18:21 am                                                                      #
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


def auth(name: str):
    """Authorizes user against resource

    Arguments:
        name: The name of the resource for which authorization is being requested.
    """
    config = Config()
    autologin = Autologin()

    try:
        # Determine if autologin has been authorized.
        auto_login = autologin.state(name)
        credentials = config.read_section(name)
    except KeyError as e:
        logger.error("The resource {} does not exist.".format(name))
        raise()

    if auto_login:
        return credentials
    else:
        user_prompt = "Please enter your user id for the {}: ".format(
            name)
        pwd_prompt = "Please enter your password for the {}: ".format(
            name)
        user = input(user_prompt)
        password = getpass(pwd_prompt)

        if user == credentials['user'] and password == credentials['password']:
            return credentials
        else:
            logger.error(
                "Invalid user id or password for {}\n".format(name))
            raise ConnectionError()


class Autologin:
    """Manages autologin for database resources."""

    def __init__(self):
        self._config = Config()

    def _check_exists(self, name) -> bool:
        if not self._config.exists(name):
            msg = "Resource {} does not exist".format(name)
            logger.error(msg)
            raise KeyError(msg)

    def state(self, name) -> bool:
        self._check_exists(name)
        result = True if 'True' in self._config.read_config(
            'AUTOLOGIN', name) else False
        return result

    def on(self, name) -> None:
        self._check_exists(name)
        self._config.write_config('AUTOLOGIN', name, 'True')

    def off(self, name) -> None:
        self._check_exists(name)
        self._config.write_config('AUTOLOGIN', name, 'False')
