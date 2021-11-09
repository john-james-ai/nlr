#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \admin.py                                                                                                     #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 1:04:27 pm                                                                         #
# Modified : Monday, November 8th 2021, 3:04:12 pm                                                                         #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
"""Global Process Administration.

This is a global object that provides a way for modules to assign projects to multiprocessing
"""
import logging
import multiprocessing as mp
from nlr.process.base import Project

# ------------------------------------------------------------------------------------------------------------------------ #
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# ------------------------------------------------------------------------------------------------------------------------ #


class ProjectAdmin:
    projects = {}

    def add_project(self, project):
        try:
            ProjectAdmin.projects[project.id] = project
            script = "{} {}".format(project.module, project.id)
            os.system(script)
        except KeyError as e:
            logger.error('Project already exists. {}'.format(e))
            raise
        except Exception as e:
            logger.error(e)
            raise

    def get_project(self, id: str) -> Project:
        try:
            project = ProjectAdmin.projects[id]
            del projects[id]
            return project
        except KeyError as e:
            logger.error('Project with id = {} does not exist.'.format(id))
            raise
        except Exception as e:
            logger.error(e)
            raise


if __name__ == '__main__':
    mp.freeze_support()
