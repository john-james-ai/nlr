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
# Modified : Monday, November 8th 2021, 8:35:23 pm                                                                         #
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
from configparser import ConfigParser

# Delete these imports
from random import randint
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------------------------------ #


class Job:
    def __init__(self, params: dict) -> None:
        self.id = str(uuid.uuid4())
        self.name = self.__class__.__name__
        self.params = params
        self.result = None

# ------------------------------------------------------------------------------------------------------------------------ #


class Project:
    def __init__(self, params: list, worker: Callable, module: str = 'parallel.py') -> None:
        self.id = str(uuid.uuid4())
        self.name = self.__class__.__name__
        self.params = params
        self.module = module
        self.worker = worker
        self.jobs = []
        self.results = []


# ------------------------------------------------------------------------------------------------------------------------ #


class Worker(ABC):
    def __init__(self, job, queue, configurer):
        self.job = job
        self.queue = queue
        self.configurer = configurer

    def run(self):
        start_time = datetime.now()

        self.configurer(self.queue)

        message = 'Worker {} started.'.format(self.job.name)
        logging.info(message)

        self.job.result = self._run()

        duration = datetime.now() - start_time
        message = "Worker {} completed in {}.".format(
            self.job.name, duration)
        logging.info(message)

    @abstractmethod
    def _run(self):
        pass


# ------------------------------------------------------------------------------------------------------------------------ #
class ProjectManager(ABC):
    """Orchestrates the execution of projects containing multiple jobs."""

    def __init__(self, project: Project, *args, **kwargs):
        self.project = project
        self._config = ConfigParser()

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

        self.project.results = self._complete(results)

        duration = datetime.now() - self.start_time

        # Start message
        message = "Project {} complete. Duration: {}.".format(
            self.project.name, duration)
        logger.info(message)

    @abstractmethod
    def _create_jobs(self, params: list) -> list:
        pass

    @abstractmethod
    def _process_results(self, jobs: list) -> Any:
        pass


# ------------------------------------------------------------------------------------------------------------------------ #
class Director(ABC):
    """Orchestrates one or more projects."""

    def __init__(self, *args, **kwargs):
        self.name = self.__class__.__name__
        self._config = ConfigParser()

    def run(self):
        start_time = datetime.now()

        # Start message
        message = "Director {} started.".format(self.name)
        logger.info(message)

        self.projects = self._run()

        # End message
        duration = datetime.now() - start_time
        message = "Director {} completed {} projects in {}.".format(
            self.name, len(self.projects), duration)
        logger.info(message)

    @abstractmethod
    def _run(self):
        pass


if __name__ == '__main__':
    mp.freeze_support()
