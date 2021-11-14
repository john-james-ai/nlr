#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \queries.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Tuesday, November 9th 2021, 8:24:49 pm                                                                        #
# Modified : Sunday, November 14th 2021, 5:25:51 pm                                                                        #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# Abstracts the physical database from the rest of the applications.
from abc import ABC, abstractmethod
import logging
import mysql.connector as cnx
from typing import Any

from nlr.database.connect import MySQLPool
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class MetadataDAO(ABC):
    """Abstract contract for database access objects. """

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def read(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs):
        pass


# ------------------------------------------------------------------------------------------------------------------------ #
class DatasetMetadataDAO(MetadataDAO):
    """Dataset metadata database access object.."""

    def __init__(self, server, pool) -> None:
        super(DatasetMetadataDAO, self).__init__(server, pool)

    def create(self, dataset_metadata: DatasetMetadata) -> None:
        self.server.initialize()

    def update(self, **kwargs):
        pass

    def read(self, **kwargs):
        pass

    def delete(self, **kwargs):
        pass


class DBAccess:
    """Provides access to the underlying databases."""

    def modify(self, query: Query, connection: cnx.connection) -> None:
        cursor = connection.cursor()
        try:
            cursor.execute(query.sql, query, params)
            cursor.close
            logger.info("Executed {}".format(query.description))
        except cnx.Error as e:
            msg = "Error occurred in query {} while inserting into the {} table. Error: {}".format(
                query.name, query.table, e)
            logger.error(msg)
            raise
        finally:
            cursor.close()

    def read(self, query: Query, connection: cnx.connection) -> Query:
        cursor = connection.cursor()
        try:
            cursor.execute(query.sql, query, params)
            query.results = cursor.fetchall()
            cursor.close
            logger.info("Executed {}".format(query.description))
        except cnx.Error as e:
            msg = "Error occurred in query {} while reading from {} table. Error: {}".format(
                query.name, query.table, e)
            logger.error(msg)
            raise
        finally:
            cursor.close()

        return query


class Query:
    """Data transfer object that encapsulates a query .

    Arguments:
        name: The name of the query
        description: Description of what the query was doing
        modulename: The name of the module in which the query originated.
        classname: The name of the class in which the query originated.
        methodname: The name of the method from which the query originated.
        resource: The database resource upon which the query was to be executed.
        query_string: The query string without parameters
        connection: The MySQL Connection
        parameters: Optional. Parameters for the query

    """

    def __init__(self, name: str, description: str, classname: str, methodname: str, resource: str, query_string: str,
                 parameters: tuple = (), arguments=None) -> None:
        self.name = name
        self.description = description
        self.classname = classname
        self.methodname = methodname
        self.resource = resource
        self.query_string = query_string
        self.parameters = parameters
        self.arguments = arguments

    def __repr__(self):
        rep = 'Query('+self.name + ',' + self.classname + ',' + self.methodname + ',' + \
            self.resource + ',' + self.query_string + ',' + \
            self.parameters + ',' + self.arguments + ')'
        return rep

    def __str__(self):
        result = ""
        attrs = self.__dict__
        for k, v in attrs.items():
            result += "\t\t{}: \t{}\n".format(k, v)
        return result

    def has_argument(self, argument) -> bool:
        answer = False
        if self.arguments:
            if argument in self.arguments.keys():
                answer = True
            else:
                answer = False
        return answer

    def get_argument(self, argument) -> Any:
        if self.has_argument(argument):
            return self.arguments[argument]
        else:
            return None
