#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \base.py                                                                                                      #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 1:20:26 am                                                                         #
# Modified : Wednesday, November 10th 2021, 11:20:38 am                                                                    #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Defines base classes for workers, managers, jobs, and directors."""
from datetime import datetime
from abc import ABC, abstractmethod
import logging
from typing import Callable, Any
import uuid
from multiprocessing.Manager import Queue

from nlr.utils.system import Profiler

# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------------------------------ #


class Job(ABC):
    """Encapsulates the parameters, processes, and results of a job.

    Arguments:
        params: Dictionary containing the parameters of the job

    """

    def __init__(self, params: dict) -> None:
        # Identifier used by resource and project management.
        self.id = str(uuid.uuid4())
        self.name = self.__class__.__name__
        self.params = params

    def setup(self) -> None:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    def teardown(self) -> None:
        pass


# ------------------------------------------------------------------------------------------------------------------------ #

# ------------------------------------------------------------------------------------------------------------------------ #


class Project:
    def __init__(self, params: list, worker: Callable) -> None:
        self.id = str(uuid.uuid4())
        self.name = self.__class__.__name__
        # List containing parameters for the project.
        self.params = params
        # The Worker callable that will execute the job.
        self.worker = worker
        self.first_job_start = None
        self.last_job_end = None
        self.project_duration = None
        self.project_cost = None
        self.jobs = []
        self.results = []


# ------------------------------------------------------------------------------------------------------------------------ #


class Worker(ABC):
    def __init__(self, job: Job, queue: Queue, configurer: Callable, results: Results):
        self.job = job
        self.queue = queue
        self.configurer = configurer
        self.results = results

    def run(self):
        self.job.start_time = datetime.now()

        self.configurer(self.queue)

        message = 'Worker {} started.'.format(self.job.name)
        logging.info(message)

        self.job.result = self._run()

        self.job.end_time = datetime.now()

        self.job.duration = self.job.end_time - self.job.start_time
        message = "Worker {} completed in {}.".format(
            self.job.name, duration)
        logging.info(message)

    @abstractmethod
    def _run(self):
        pass

# ------------------------------------------------------------------------------------------------------------------------ #


class Results:
    """Object to capture Job results. This is encapsulated inside the Job object."""

    def __init__(self):
        self.worker = None          # Name of worker object assigned during job execution
        self.process = None         # Process name that executed the job
        self.start_time = None
        self.end_time = None
        self.duration = None
        # Results are also encapsulated within the job.
        self.result = None
# ------------------------------------------------------------------------------------------------------------------------ #


class Manager(ABC):
    """Orchestrates the execution of projects containing multiple jobs."""

    def __init__(self, project: Project, *args, **kwargs):
        self.project = project

    def create_jobs(self):

        # Start message
        message = "Project {} creating jobs.".format(self.project.name)
        logger.info(message)

        # Create jobs
        self.project.jobs = self._create_jobs(self.project.params)

        message = "{} created {} jobs.".format(
            self.__class__.__name__, len(self.project.jobs))
        logger.info(message)

    def process_results(self, results: list):

        # Start message
        message = "Project {} compiling results.".format(self.project.name)
        logger.info(message)

        self.project.results = self._process_results(results)

        duration = datetime.now() - self.start_time

        # Start message
        message = "Project {} complete. Duration: {}.".format(
            self.project.name, duration)
        logger.info(message)

    @abstractmethod
    def _create_jobs(self, params: list) -> list:
        pass

    @abstractmethod
    def _process_results(self, results: list) -> Any:
        pass


# ------------------------------------------------------------------------------------------------------------------------ #
class Builder(ABC):
    """Abstraction for building the data."""

    @property
    @abstractmethod
    def data(self) -> None:
        pass

    @abstractmethod
    def build_metadata(self) -> None:
        pass

    @abstractmethod
    def extract_data(self) -> None:
        pass

    @abstractmethod
    def explore_data(self) -> None:
        pass

    @abstractmethod
    def clean_data(self) -> None:
        pass

    @abstractmethod
    def transform_data(self) -> None:
        pass


# ------------------------------------------------------------------------------------------------------------------------ #
class BuilderRatings(BUILDER):
    """Builds ratings data."""

    @property
    def data(self) -> None:
        pass

    def build_metadata(self) -> None:
        pass

    def extract_data(self) -> None:
        pass

    def explore_data(self) -> None:
        pass

    def clean_data(self) -> None:
        pass

    def transform_data(self) -> None:
        pass
# ------------------------------------------------------------------------------------------------------------------------ #


class BuilderReviews(Builder):
    """Builds reviews data."""

    @property
    def data(self) -> None:
        pass

    def build_metadata(self) -> None:
        pass

    def extract_data(self) -> None:
        pass

    def explore_data(self) -> None:
        pass

    def clean_data(self) -> None:
        pass

    def transform_data(self) -> None:
        pass


class Director(ABC):
    """Orchestrates the data building process via delegation to a builder object."""

    def __init__(self, resource_manager: ResourceManager):
        self.name = self.__class__.__name__
        self._builder = None
        self._resource_manager = resource_manager

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        self._builder = builder

    def build_ratings_data(self) -> None:
        self._builder.build_metadata()
        self._builder.extract_data()
        self._builder.explore_data()
        self._builder.clean_data()
        self._builder.transform_data()

    def build_reviews_data(self) -> None:
        self._builder.build_metadata()
        self._builder.extract_data()
        self._builder.explore_data()
        self._builder.clean_data()
        self._builder.transform_data()


if __name__ == '__main__':
    mp.freeze_support()
