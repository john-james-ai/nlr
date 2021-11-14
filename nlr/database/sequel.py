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
# Modified : Sunday, November 14th 2021, 4:48:10 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Module for database and table creation data definition language in the form dictionaries."""

TABLES = {}
TABLES['datasource'] = """
CREATE TABLE IF NOT EXISTS datasource(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    extracted TINYINT(1) NOT NULL,
    category VARCHAR(100) NOT NULL,
    category_label VARCHAR(100) NOT NULL,
    label VARCHAR(200) NOT NULL,
    type VARCHAR(20) NOT NULL,
    n INT NOT NULL,
    size INT,
    download_size INT,
    url VARCHAR(400) NOT NULL,
    filename VARCHAR(100) NOT NULL,
    file_ext VARCHAR(10) NOT NULL,
    active TINYINT(1) NOT NULL,
    download_start DATETIME,
    download_end DATETIME,
    download_duration INT,
    updated DATETIME
)
"""

TABLES['dataset'] = """
CREATE TABLE IF NOT EXISTS dataset(
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    stage VARCHAR(10) NOT NULL,
    filename VARCHAR(100) NOT NULL,
    category VARCHAR(100) NOT NULL,
    type VARCHAR(100) NOT NULL,
    n INT NOT NULL,
    size INT,
    created DATETIME,
    updated DATETIME
)
"""

SEQUEL = {}
SEQUEL['datasource'] = {
    'create_table':
        {
            'name': 'create_table',
            'description': 'Creates the datasource table',
            'table': 'datasource',
            'qtype': 'create_table',
            'sql': TABLES['datasource'],
        },
    'select_all':
        {
            'name': 'select_all',
            'description': 'Select all data from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT * from datasource"""
        },
    'select_category':
        {
            'name': 'select_category',
            'description': 'Select all data from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT * from datasource WHERE category = %s"""
        },
    'select_url':
        {
            'name': 'select_url',
            'description': 'Select url from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT url from datasource WHERE id = %s"""
        },
    'select_active':
        {
            'name': 'select_active',
            'description': 'Select active from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT active from datasource WHERE id = %s"""
        },
    'select_type':
        {
            'name': 'select_type',
            'description': 'Select all data from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT * from datasource WHERE type = %s""",
        },
    'select_category_type':
        {
            'name': 'select_category_type',
            'description': 'Select all data from datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT * from datasource WHERE category = %s AND type = %s""",
        },
    'select_count':
        {
            'name': 'select_count',
            'description': 'Select the number of rows in the datasource table',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT COUNT(*) from datasource""",
        },
    'select_size':
        {
            'name': 'select_size',
            'description': 'Select the size of a datasource',
            'table': 'datasource',
            'qtype': 'select',
            'sql': """SELECT size from datasource WHERE id = %s""",
        },
    'insert':
        {
            'name': 'insert_datasource',
            'description': 'Insert data into the datasource table.',
            'table': 'datasource',
            'qtype': 'insert',
            'sql': """INSERT INTO datasource (extracted, category, category_label, label, type, n, url, filename, file_ext, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        },
    'update':
        {
            'size':
                {
                    'name': 'update_size',
                    'description': 'Update the size of a datasource.',
                    'table': 'datasource',
                    'qtype': 'update',
                    'sql': """UPDATE datasource SET size = %s WHERE id = %s""",
                },
            'download':
                {
                    'name': 'download_update',
                    'description': 'Update datasource download metadata.',
                    'table': 'datasource',
                    'qtype': 'update',
                    'sql': """UPDATE datasource SET
                                download_size = %s,
                                download_start = %s,
                                download_end = %s,
                                download_duration = %s,
                                updated = %s
                            WHERE id = %s"""
                },
            'active':
                {
                    'name': 'update_active',
                    'description': 'Update the datasource active variable.',
                    'table': 'datasource',
                    'qtype': 'update',
                    'sql': """UPDATE datasource SET active = %s WHERE id = %s"""
                }
        },
        'drop':
        {
            'name': 'drop',
            'description': 'Drop datasource table.',
            'table': 'datasource',
            'qtype': 'drop',
            'sql': """DROP TABLE IF EXISTS datasource""",
        },
        'delete':
        {
            'name': 'delete',
            'description': 'Delete from datasource table.',
            'table': 'datasource',
            'qtype': 'delete',
            'sql': """DELETE FROM datasource WHERE id = %s""",
        },
        'exists':
        {
            'name': 'exists',
            'description': 'Checks existence of row in datasource table based on id.',
            'table': 'datasource',
            'qtype': 'exists',
            'sql': """SELECT EXISTS(SELECT 1 FROM datasource WHERE id = %s)""",
        },
        'exists_category':
        {
            'name': 'exists',
            'description': 'Checks existence of row in datasource table based on id.',
            'table': 'datasource',
            'qtype': 'exists',
            'sql': """SELECT EXISTS(SELECT 1 FROM datasource WHERE category = %s)""",
        },


}
