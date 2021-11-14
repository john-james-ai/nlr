#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \builder.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Wednesday, November 10th 2021, 3:14:29 am                                                                     #
# Modified : Wednesday, November 10th 2021, 11:29:15 pm                                                                    #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Encapsulates the process of building the datasets."""
from abc import ABC, abstractmethod
import logging

from nlr.data.base import Director
# ------------------------------------------------------------------------------------------------------------------------ #
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------------------------------------------------------------ #
class DatasetBuilder(ABC):
    """Abstract dataset builder class.

    The DatasetBuilder class specifies the methods for obtaining, ingesting, processing, and presenting datasets for modeling.
    """

    def __init__(self, dao: DatasetMetadataDAO)

    @property
    @abstractmethod
    def build_metadata(self) -> None:
        pass

    @abstractmethod
    def extract(self) -> None:
        pass

    @abstractmethod
    def explore(self) -> None:
        pass

    @abstractmethod
    def clean(self) -> None:
        pass

    @abstractmethod
    def transform(self) -> None:
        pass

    @abstractmethod
    def combine(self) -> None:
        pass

    @abstractmethod
    def split(self) -> None:
        pass

    @abstractmethod
    def combine(self) -> None:
        pass

# ------------------------------------------------------------------------------------------------------------------------ #


class DatasetBuilderRatings(DatasetBuilder):
    """Builder rating datasets. """

    @property
    @abstractmethod
    def build_metadata(self) -> None:
        pass

    @abstractmethod
    def extract(self) -> None:
        pass

    @abstractmethod
    def explore(self) -> None:
        pass

    @abstractmethod
    def clean(self) -> None:
        pass

    @abstractmethod
    def transform(self) -> None:
        pass

    @abstractmethod
    def combine(self) -> None:
        pass

    @abstractmethod
    def split(self) -> None:
        pass

    @abstractmethod
    def combine(self) -> None:
        pass
