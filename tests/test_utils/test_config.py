#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \test_config.py                                                                                               #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 11:29:19 pm                                                                        #
# Modified : Tuesday, November 9th 2021, 12:24:15 pm                                                                       #
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

from nlr.utils.config import Config
# ------------------------------------------------------------------------------------------------------------------------ #
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfigTests:

    def test_read_config(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()
        assert config.read_config(section='DATASOURCE', option='bucketname') == 'nlr-data', "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_write_config(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()

        config.write_config('WRITE', 'test1', 'value1')
        config.write_config('WRITE', 'test2', 'value2')
        value = config.read_config('WRITE', 'test1')

        assert value == 'value1', "Failure in {} local data metadata {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_write_configs(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        section = 'WRITE_CONFIGS'
        options = ["option_{}".format(i) for i in range(5)]
        values = ["value_{}".format(i) for i in range(5)]

        config = Config()
        config.write_configs(section, options, values)

        for i in range(len(options)):
            assert config.read_config(section, options[i]) == values[i], "Failure in {} local data metadata {}".format(
                inspect.stack()[0][3])

        config.remove_section(section)

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_remove_option(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()
        config.remove_option('WRITE', 'test2')

        with pytest.raises(KeyError):
            assert config.read_config('WHITE', 'test2'), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_remove_section(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()
        config.remove_section('WRITE')

        with pytest.raises(KeyError):
            assert config.read_config('WHITE', 'test2'), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_write_options(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        options = []
        for i in range(5):
            option = {}
            k = 'key_' + str(i)
            v = 'value_' + str(i)
            option[k] = v
            options.append(option)

        config = Config()
        config.write_options('OPTIONS', options)

        for option in options:
            for k, v in option.items():
                assert config.read_config('OPTIONS', k) == v, "Failure in {}".format(
                    inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_read_section_as_dict(self):

        config = Config()
        options = config.read_section('OPTIONS', as_dict=True)
        keys = list(options.keys())
        values = list(options.values())
        for i in range(len(keys)):
            assert keys[i] == 'key_' + str(i), "Failure in {}".format(
                inspect.stack()[0][3])
            assert values[i] == 'value_' + str(i), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_read_section(self):

        config = Config()
        options = config.read_section('OPTIONS', as_dict=False)

        assert isinstance(options, list), "Failure in {}".format(
            inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_print_section(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()
        config.print_section('OPTIONS')

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

    def test_teardown(self):
        logger.info("    Started {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))

        config = Config()
        config.remove_section('OPTIONS')
        with pytest.raises(KeyError):
            assert config.read_section('OPTIONS'), "Failure in {}".format(
                inspect.stack()[0][3])

        logger.info("    Successfully completed {} {}".format(
            self.__class__.__name__, inspect.stack()[0][3]))


if __name__ == "__main__":
    t = ConfigTests()
    t.test_read_config()
    t.test_write_config()
    t.test_write_configs()
    t.test_remove_option()
    t.test_remove_section()
    t.test_write_options()
    t.test_print_section()
    t.test_read_section_as_dict()
    t.test_read_section()
    t.test_teardown()


# %%
