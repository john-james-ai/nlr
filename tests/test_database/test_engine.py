#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_engine.py                                                                                               #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Saturday, November 13th 2021, 1:28:09 pm                                                                      #
# Modified : Sunday, November 14th 2021, 4:53:13 pm                                                                        #
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

from nlr.database.engine import DBEngine, Query
from nlr.database.sequel import SEQUEL
from nlr.database.connect import MySQLDatabase
from nlr.database.admin import TableAdmin
# ------------------------------------------------------------------------------------------------------------------------ #

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QueryGen:

    def get_sources(self):
        sources = []
        for i in range(10):
            source = tuple((
                i,
                'category_' + str(i),
                'Category_' + str(i),
                'Category Ratings for ' + str(i),
                'ratings',
                str(i+1000),
                'https://wwww.somewebsite.com',
                'somefilename',
                '.csv',
                i
            ))
            sources.append(source)
        return sources

    def get_query(self, qtype: str) -> Query:
        if qtype == 'select':
            sequel = SEQUEL['datasource']['select_category']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Select Class',
                          methodname='Some Select Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=('electronics',),
                          arguments=None)

        elif qtype == 'select_all':
            sequel = SEQUEL['datasource']['select_all']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Select Class',
                          methodname='Some Select Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(),
                          arguments=None)

        elif qtype == 'insert':
            sequel = SEQUEL['datasource']['insert']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Insert Class',
                          methodname='Some Insert Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(0, 'electronics', 'Electronics', 'Electronics Ratings',
                                      'ratings', 32902, 'http://www.someurl.com', 'somefilename', '.csv', 1),
                          arguments={'exists_ok': True})
        elif qtype == 'create':
            sequel = SEQUEL['datasource']['create_table']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Create Table Class',
                          methodname='Some Create Table Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(),
                          arguments=None)

        elif qtype == 'load':
            sequel = SEQUEL['datasource']['insert']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Insert Class',
                          methodname='Some Insert Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=self.get_sources(),
                          arguments=None)

        elif qtype == 'update':
            sequel = SEQUEL['datasource']['update']['download']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Update Class',
                          methodname='Some Update Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(
                              32320, '11/13/21 at 1349', '11/13/21 at 1449', 2323, '11/13/21 at 1449', 2),
                          arguments=None)
        elif qtype == 'drop':
            sequel = SEQUEL['datasource']['drop']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Drop Class',
                          methodname='Some Drop Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(),
                          arguments=None)
        elif qtype == 'delete':
            sequel = SEQUEL['datasource']['delete']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Delete Class',
                          methodname='Some Delete Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=('1',),
                          arguments=None)

        elif qtype == 'exists':
            sequel = SEQUEL['datasource']['exists_category']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Exists Class',
                          methodname='Some Exists Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=('electronics',),
                          arguments=None)
        elif qtype == 'exists_1':
            sequel = SEQUEL['datasource']['exists']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Exists Class',
                          methodname='Some Exists Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(1,),
                          arguments=None)
        elif qtype == 'count':
            sequel = SEQUEL['datasource']['select_count']
            query = Query(name=sequel['name'],
                          description=sequel['description'],
                          classname='Some Count Class',
                          methodname='Some Count Method',
                          resource=sequel['table'],
                          query_string=sequel['sql'],
                          parameters=(),
                          arguments=None)
        else:
            logger.error("Unrecognized Query Request")
        return query


class DBEngineTests:

    def test_drop(self):

        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        connection = MySQLDatabase().get_connection('nlr')

        qg = QueryGen()
        drop = qg.get_query('drop')

        engine = DBEngine()
        engine.write(drop, connection)

        connection.commit()
        connection.close()

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_create(self):

        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        connection = MySQLDatabase().get_connection('nlr')

        qg = QueryGen()
        create = qg.get_query('create')

        engine = DBEngine()
        engine.write(create, connection)

        connection.commit()
        connection.close()

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_load(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        connection = MySQLDatabase().get_connection('nlr')

        qg = QueryGen()
        load = qg.get_query('load')
        check = qg.get_query('count')

        engine = DBEngine()
        engine.load(load, connection)
        count = engine.read(check, connection)

        assert count[0][0] == len(load.parameters), "Failure in {}. Expected {} rows. Read {} rows".format(
            inspect.stack()[0][3], len(load.parameters), count)

        connection.commit()
        connection.close()

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_read(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        connection = MySQLDatabase().get_connection('nlr')

        qg = QueryGen()
        read = qg.get_query('select_all')

        engine = DBEngine()
        results = engine.read(read, connection)

        assert len(results) == 10,  "Failure in {}".format(
            inspect.stack()[0][3])
        assert isinstance(results, list), "Failure in {}".format(
            inspect.stack()[0][3])
        for result in results:
            assert isinstance(result, tuple), "Failure in {}".format(
                inspect.stack()[0][3])

        connection.commit()
        connection.close()

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_write(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        connection = MySQLDatabase().get_connection('nlr')

        qg = QueryGen()
        insert = qg.get_query('insert')
        check = qg.get_query('exists')

        engine = DBEngine()
        engine.write(insert, connection)
        assert engine.read(check, connection), "Failure in {}".format(
            inspect.stack()[0][3])

        connection.commit()
        connection.close()

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


def test_dbengine():
    logger.info(" Started DBEngine Tests")
    t = DBEngineTests()
    t.test_drop()
    t.test_create()
    t.test_load()
    t.test_read()
    t.test_write()

    logger.info(" Completed DBEngine Tests. Success!")


if __name__ == "__main__":
    test_dbengine()

    # %%
