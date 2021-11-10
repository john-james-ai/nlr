#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \ddl.py                                                                                                       #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 9:00:56 pm                                                                         #
# Modified : Tuesday, November 9th 2021, 7:12:01 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module for database and table creation data definition language in the form dictionaries."""

TABLES = {}
TABLES['datasources'] = """
CREATE TABLE IF NOT EXISTS datasources(
    id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50),
    type VARCHAR(20),
    active TINYINT(1),
    n INT,
    size INT,
    url VARCHAR(200),
    filename VARCHAR(50),
    filext VARCHAR(10),
    s3 TINYINT(1)
)
"""
