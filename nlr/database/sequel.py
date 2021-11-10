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
# Modified : Tuesday, November 9th 2021, 11:55:55 pm                                                                       #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module for database and table creation data definition language in the form dictionaries."""

TABLES = {}
TABLES['datasources'] = """
CREATE TABLE IF NOT EXISTS datasources(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    key VARCHAR(50) NOT NULL,
    category VARCHAR(100) NOT NULL,
    category_label VARCHAR(100) NOT NULL,
    label VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL,
    n INT NOT NULL,
    size INT,
    url VARCHAR(400) NOT NULL,
    filename VARCHAR(100) NOT NULL,
    file_ext VARCHAR(10) NOT NULL,
    active TINYINT(1) NOT NULL,
    download_size INT,
    download_start DATETIME,
    download_end DATETIME,
    download_duration,
    last_updated DATETIME
)
"""
DATASOURCES = {
    'select':
        {
            'name': 'select_all',
            'description': 'Select all data from datasources table',
            'table': 'datasources',
            'qtype': 'select',
            'sql': """SELECT * from datasources""",
            'params': ()
        },
    'insert':
        {
            'name': 'insert_datasource',
            'description': 'Insert data into the datasources table.',
            'table': 'datasources',
            'qtype': 'insert',
            'sql': """INSERT INTO datasources (key, category, category_label, label, type, n, url, filename, file_ext, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            'params': ()
        },
    'update':
        {
            'size':
                {
                    'name': 'update_size',
                    'description': 'Update the size of a datasource.',
                    'table': 'datasources',
                    'qtype': 'update',
                    'sql': """UPDATE datasources SET size = %s WHERE id = %s""",
                    'params': ()
                },
            'download':
                {
                    'name': 'download_update',
                    'description': 'Update datasource download metadata.',
                    'table': 'datasources',
                    'qtype': 'update',
                    'sql': """UPDATE datasources SET
                                download_size = %s,
                                download_start = %s,
                                download_end = %s,
                                download_duration = %s,
                                last_updated = %s
                            WHERE id = %s""",
                    'params': ()
                },
            'active':
                {
                    'name': 'update_active',
                    'description': 'Update the datasource active variable.',
                    'table': 'datasources',
                    'qtype': 'update',
                    'sql': """UPDATE datasources SET active = %s WHERE id = %s""",
                    'params': ()
                }
        }
}
