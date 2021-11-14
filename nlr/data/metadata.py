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
# Modified : Wednesday, November 10th 2021, 11:01:21 pm                                                                    #
# Modifier : John James (john.james@nov8.ai)                                                                               #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Scripts associated with sourcing data."""
# %%
from abc import ABC, abstractmethod
from datetime import datetime
from copy import copy
import os
import logging
from configparser import ConfigParser
import boto3
import botocore
import multiprocessing as mp
from typing import Any

from nlr.data.base import Director, Worker, Manager, Job, Project
from nlr.process.admin import ProjectAdmin
from nlr.utils.files import get_filenames
from nlr.database.access import DatasetMetadataDAO

# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------------------------------------------------ #


class MetadataBase(ABC):
    """Abstract base class for metadata"""

    def __init__(self, *args, **kwargs) -> None:
        self.id
        self.name
        self.description
        self.created = datetime.now()
        self.updated = None
        self.version = 0

    @abstractmethod
    def equal(self, object: Any) -> bool:
        """Determines whether the specified object is equal to the current object."""
        pass

    @abstractmethod
    def get_type(self) -> Any:
        """Returns the class type for the current instance."""
        pass

    @abstractmethod
    def clone(self) -> Any:
        """Performs memberwise shallow copy of current object."""

    @abstractmethod
    def load(self) -> None:
        """Loads the metadata from back-end storage."""
        pass

    @abstractmethod
    def save(self) -> None:
        """Saves metadata to the back-end data storage."""
        pass


class DatasetMetadata(MetadataBase):
    """Base class for a data sets."""

    def __init__(self, name: str, dao: DatasetMetadataDAO, description: str = None,
                 local_directory: str = None, uri: str = None) -> None:
        super(DatasetMetadata, self).__init__(name, description)
        self.dao = dao
        self.uri = uri
        self.filename = os.path.basename(uri) if uri else None
        self.filetype = None
        self.file_content = None                            # Rating or review
        self.file_ext = os.path.splitext(uri) if uri else None
        self.local_directory = local_directory
        self.features = None
        self.dependent_variable = None
        self.size = 0
        self.download_size = 0

    def __eq__(self, dataset_metadata: DatasetMetadata) -> bool:
        """Determines whether the specified object is equal to the current object."""
        return self.__dict__ == dataset_metadata.__dict__

    def get_type(self) -> Any:
        """Returns the class type for the current instance."""
        return self.__class__.__name__

    def clone(self) -> Any:
        """Performs memberwise shallow copy of current object."""
        ds = DatasetMetadata(self.name, self.description, self.local_directory,
                             self.uri)
        ds.filename = copy(self.filename)
        ds.filetype = copy(self.filetype)
        ds.file_content = copy(self.file_content)
        ds.file_ext = copy(self.file_ext)
        ds.local_directory = copy(self.local_directory)
        ds.feature = copy(self.features)
        ds.dependent_variable = copy(self.dependent_variable)
        ds.size = copy(self.size)
        ds.download_size = copy(self.download_size)
        return ds

    def load(self) -> None:
        try:
            mdds = self.dao.read_by_id(self.id)
            for k, v in mdds.items():
                self.__dict__[k] = v
        except Exception as e:
            logger.error(e)

    def save(self, dataset_metadata_dao: DatasetMetadataDAO) -> None:
        try:
            self.dao.write(self)
        except Exception as e:
            logger.error(e)


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
