#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \file.py                                                                                                      #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 3:39:51 pm                                                                         #
# Modified : Monday, November 8th 2021, 9:51:01 pm                                                                         #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""File utilities."""
import os
from configparser import ConfigParser
# ------------------------------------------------------------------------------------------------------------------------ #


def get_absdir(basedir: str) -> str:
    """Returns absolute path to the designate base directory """
    """Returns filenames in a directory specified by its basename. """
    config = ConfigParser()
    config.read(configfile)
    folder = config['PATH'][basename]
    return folder


def get_filepaths(basedir: str) -> list:
    """Returns a list of absolute filepaths for each file in the designated base directory."""
    absdir = get_absdir(basedir)
    filenames = get_filenames(basedir)
    filepaths = [os.path.join(absdir, filename) for filename in filenames]
    return filepaths


def get_filenames(basedir: str) -> list:
    """Returns filenames in a directory specified by its basename. """
    config = ConfigParser()
    config.read(configfile)
    folder = config['PATH'][basename]
    filenames = os.path.listdir(folder)
    return filenames
