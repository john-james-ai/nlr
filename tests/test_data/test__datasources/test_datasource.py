#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_datasource.py                                                                                           #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 3:44:04 am                                                                         #
# Modified : Monday, November 8th 2021, 5:10:02 am                                                                         #
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
# from importlib import reload
# logging.shutdown()
# reload(logging)
from nlr.data.sources import DataSource
# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataSourceTests:

    def test_get_filenames(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        ds = DataSource()
        filenames = ds.get_filenames()
        assert isinstance(filenames, list), "Failure in {}".format(
            inspect.stack()[0][3])
        assert len(filenames) > 7, "Failure in {} ".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_bucket_exists(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        ds = DataSource()
        assert ds.s3_bucket_exists(), "Failure in {} S3 bucket doesn't exist".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_local_metadata(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        ds = DataSource()
        meta = ds.get_metadata(local=True)

        assert isinstance(meta, dict), "Failure in {} local data metadata {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_remote_metadata(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        ds = DataSource()
        meta = ds.get_metadata(local=False)

        assert isinstance(meta, dict), "Failure in {} local data metadata {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = DataSourceTests()
    t.test_get_filenames()
    t.test_bucket_exists()
    t.test_local_metadata()
    t.test_remote_metadata()


# %%
