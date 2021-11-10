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
# Modified : Wednesday, November 10th 2021, 3:32:54 am                                                                     #
# Modifier : John James (john.james@nov8.ai)                                                                               #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Scripts associated with sourcing data."""
# %%
from abc import ABC, abstractmethod
import os
import logging
from configparser import ConfigParser
import boto3
import botocore
import multiprocessing as mp


from nlr.data.base import Director, Worker, Manager, Job, Project
from nlr.process.admin import ProjectAdmin
from nlr.utils.files import get_filenames

# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


class DownloadResponse:
    start = None
    end = None
    duration = None
    destination = None
    source = None
    force = None
    code = None
    message = None
    metadata = None


class DataSource(ABC):
    """Base class for a data source."""

    def __init__(self, name: str, *args, **kwargs):
        self.name = name
        self._config = ConfigParser()
        self.response = DownloadResponse()

    @abstractmethod
    def connect(self) -> bool:
        pass

    @abstractmethod
    def bucket_exists(self) -> bool:
        pass

    @abstractmethod
    def object_exists(self) -> bool:
        pass

    @abstractmethod
    def download(self, source: str, destination: str, force: bool = False) -> dict:
        """Downloads a single file / object from an S3 bucket.

        Arguments:
            source: The uri, filename or url for the source data.
            destination: The expanded directory to which data is to be downloaded.
            force: If True, local data, if exists are overwritten
        """
        pass

    @abstractmethod
    def get_metadata(self) -> dict:
        pass

    @abstractmethod
    def get_inventory(self) -> list:
        pass


class S3DataSource(DataSource):
    """S3 Data Source .

    Arguments:
        name: This name uniquely identifies the data source and the access credentials. Note, access credentials must
            be stored in the config.ini file for the project under this name.
        bucketname: The name of the S3 bucket containing the data.

    """

    def __init__(self, name: str, bucketname: str) -> None:
        super(S3DataSource, self).__init__(name)
        self._bucketname = bucketname
        self._s3 = None

    def _final_response(self, code: int, message: str) -> None:
        self.response.end = datetime.now()
        self.response.duration = self.response.end - self.response.start
        self.response.code = code
        self.response.message = message

    def connect(self) -> bool:
        success = True
        self._config.read(configfile)
        try:
            self._s3 = boto3.resource('s3',
                                aws_access_key_id=self._config['NLR-USER']['access_key'],
                                aws_secret_access_key=self._config['NLR-USER']['secret_key'])
        except Exception as e:
            self._final_response('401', e)
            return False

        return True

    def bucket_exists(self) -> bool:
        exists = True
        if not self._s3 and not self.connect():
            return False
        else:
            try:
                self._s3.meta.client.head_bucket(Bucket=self._bucketname)
            except botocore.exceptions.ClientError as e:
                # If a client error is thrown, then check that it was a 404 error.
                # If it was a 404 error, then the bucket does not exist.
                error_code = e.response['Error']['Code']
                exists = False
            return exists

    def object_exists(self, source: str) -> bool:
        objects = self.get_inventory()
        return source in objects

    def get_inventory(self) -> list:
        """Returns a list of object names in a bucket."""
        objects = []
        if self.bucket_exists():
            bucket = self._s3.Bucket(self._bucketname)
            for key in bucket.objects.all():
                objects.append(key)
        return objects

    def download(self, source: str, destination: str, force: bool = False) -> dict:
        """Downloads a single file / object from an S3 bucket.

        Arguments:
            source: The uri, filename or url for the source data.
            destination: The expanded directory to which data is to be downloaded.
            force: If True, local data, if exists are overwritten
        """
        # Initialize the response ojbect.
        self.response = DownloadResponse()
        self.response.start = datetime.now()
        self.response.destination = destination
        self.response.source = source
        self.response.force = force

        filenames = self.get_inventory()
        if source not in filenames:
            self.response.end = datetime.now()
            self.response.duration = self.response.end - self.response.start
            self.response.code = 404
            self.response.message = "{} not found".format(source)
            return self.response

        filepath = os.path.join(destination, source)
        if os.path.exists(filepath) and not force:
            response.end = datetime.now()
            response.duration = response.end - response.start
            response.code = 304
            response.message = "{} already exists and force = False".format(
                source)
            return response

            response['force'] = force

        start_time = datetime.now()

        for objectname in object_names:

    def exists_locally(self, destination, objectname) -> bool:
        return

        # Confirm named datasets (object names) are valid
        if datasets:
            valid = [dataset in object_names for dataset in datasets]

        os.makedirs(destination, exist_ok=True)

        object_names = self.get_inventory()
        if datasets:
            all_valid = [dataset in object_names datasets]
        if not dataset
        #
        if not dataset:

    def load_metadata(self) -> None:
        s3 = self._connect()
        if self._exists(s3):
            self._metadata = self._load_metadata(s3)

    def _connect(self):
        """Connects to an S3 instance and returns a bucket object."""

    def _exists(self, s3) -> bool:

    def _load_metadata(self, s3):
        """Retrieves metadata for an S3 bucket"""

        bucket = s3.Bucket(self._bucketname)
        for key in bucket.objects.all():
            self._metadata[key.key] = s3.meta.client.head_object(Bucket=self._bucketname,
                                                             key=key.key)

    def get_metadata(self) -> dict:
        """Returns available metadata"""
        if not self._metadata:
            self.load_metadata()
        return self._metadata

    def get_inventory(self) -> list:
        """Returns a list of S3 object keys/names in the S3 bucket."""
        if not self._metadata:
            self.load_metadata()
        keys = [key for key in self.metadata.keys()]
        return keys


# ------------------------------------------------------------------------------------------------------------------------ #
class DataSourceManager(Manager):

    def __init__(self, project: Project):
        super(DataSourceManager, self).__init__(project)

    def _create_jobs(self) -> list:
        jobs = []

        # Get names of files in raw directory if any exist
        filepaths = get_filepaths('raw')

           # For each file, we mark it for download if force is True or no local exists.
           for filepath in filepaths:
                download = False
                download = True if self.force else False
                download = True if not os.path.exists(filepath) else False

                if download:

                    job = Job(para)

            if self.force or len(filenames) == 0:
                download = True

        # For each file, download if force is True or no local copy exists.
        for filename in params:
            download = False

            d['filename'] = filename
            d['filepath'] = os.path.join(raw_folder, filename)

            if filename in local_filenames and self.force:
                overwrite = input(
                    "File {} already exists locally. Force will overwrite the local copy.\nType 'force' to confirm that authorization to overwrite the local file with the remote source.") or None

                if overwrite == 'force':
                    download = True

            elif filename not in local_filenames:
                download = True

        # If the file has been marked for download, create the job.
        if download:
            job = Job(params=d)
            jobs.append(job)

        return jobs



# ------------------------------------------------------------------------------------------------------------------------ #
class DataDirector(Director):

    def __init__(self):
        super(DataDirector, self).__init__()

    def get_source_data(self) -> None:
        """Obtains the source data and stores in destination

        Arguments:
            source: Name of the source


if __name__ == '__main__':
    mp.freeze_support()
