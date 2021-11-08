#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \sources.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james@nov8.ai                                                                                            #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Sunday, November 7th 2021, 5:42:49 pm                                                                         #
# Modified : Sunday, November 7th 2021, 11:17:50 pm                                                                        #
# Modifier : John James (john.james@nov8.ai)                                                                               #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Scripts associated with sourcing data."""
# %%
import logging
from configparser import configparser
import boto3
import botocore

from nlr.setup import configfile
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class DataSources:

    def __init__(self):
        self._config = configparser.ConfigParser()
        self._bucketname = None
        self._bucket = None
        self._keys = []
        self._s3 = None
        self._data_source_exists = None
        self._bucket_exists = None

    def get_data_home(self):
        self._config.read(DataSources.configfile)
        data_home = self._config['PATH']['data_home']
        if not data_home:
            logger.warn("Data home not set.")
            return None
        else:
            return data_home

    def set_data_home(self, path):
        """Sets data home relative to user's home directory."""

    def get_data_source_path(self):
        self._config.read(DataSources.configfile)

        try:
            folder = self._config['PATH']['raw_data_path']
            return folder
        except KeyError as e:
            logger.warn("Data source folder not designated")

        return folder

    def set_data_source_path(self, path):
        """Sets the local path of the data source relative to data_home."""
        data_home = self.get_data_home()
        if not data_home:
            logger.info("Please set the home directory for data.")
        self._config.read(DataSources.configfile)
        SELF._config.set('PATH', 'raw_data_path', path)
        with open(DataSources.configfile, 'wb') as configfile:
            self._config.write(configfile)

    def s3_bucket_exists(self):
        """Checks existence of S3 bucket containing the source data. Also populates self._bucket attribute."""
        self._config.read(DataSources.configfile)
        self._bucketname = self._config['NLR-USER']['bucket']

        self._s3 = bobo3.resource('s3')
        self._bucket = self._s3.Bucket(self._bucketname)
        exists = True
        try:
            self._s3.meta.client.head_bucket(Bucket=self._bucketname)
        except botocore.exceptions.ClientError as e:
            # If a client error is thrown, then check that it was a 404 error.
            # If it was a 404 error, then the bucket does not exist.
            error_code = e.response['Error']['Code']
            if error_code == '404':
                exists = False
            else:
                logger.error("Error connecting with S3 resource. {}".format(e))
                raise Exception(e)

        return exists

    def _get_local_metadata(self):
        """Retrieves metadata from local source if available, otherwise, returns an empty dictionary."""
        metadata = {}
        self._config.read(DataSources.configfile)
        raw_data_path = self._config['PATH'].get('raw_data_path', None)
        if not raw_data_path:
            logger.info("No local raw data folder designated.")
            return metadata
        elif not os.path.exists(raw_data_path):
            logger.info("The raw data folder does not exist.")
            return metadata
        elif len(os.listdir(raw_data_path)) == 0:
            logger.info("The raw data folder is empty.")
            return metadata
        else:

            filenames = os.listdir(raw_data_path)
            for filename in filenames:
                metadata[filename] = os.stat(
                    os.path.join(raw_data_path, filename))

            return metadata

    def _get_remote_metadata(self):
        """Retrieves metadata from S3 resource, or an empty dictionary if no data sources exist."""
        metadata = {}
        if self._bucket_exists():
            for key in self._bucket:
                metadata[key] = self._s3.meta.client.head_object(Bucket=self._bucketname,
                                                                 Key=key)
        return metadata

    def get_metadata(self, local=True):
        """Get metadata the data sources."""
        if local:
            return self._get_local_metadata()
        else:
            return self._get_remote_metadata()

    def download(self, data_home=None):

        if not data_home:
            data_home = self._config.get('data_home', None)
            if not data_home:
                data_home = input(
                    "Please enter your home data directory relative to your home directory.", os.path.join("~", "nlr_data"))
        data_home = os.path.expanduser(data_home)
        os.makedirs(data_home, exist_ok=True)
