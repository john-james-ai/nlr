#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \parallel.py                                                                                                  #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Monday, November 8th 2021, 12:18:21 am                                                                        #
# Modified : Tuesday, November 9th 2021, 12:32:19 am                                                                       #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import argparse
import math
import os
import logging
import logging.handlers
import multiprocessing as mp
import time
import numpy as np
import pandas as pd


from nlr.utils.loggers import LogFile
#from nlr.process.admin import ProjectAdmin
# ------------------------------------------------------------------------------------------------------------------------ #
NUM_PROCESSORS = max(1, int(math.floor(mp.cpu_count()/2)))

# ------------------------------------------------------------------------------------------------------------------------ #


def listener_configurer():
    """Top-level loop that waits for logging events on the queue until the LogRecords is None."""
    root = logging.getLogger()
    lf = LogFile()
    logfilepath = lf.get_logfile(logname='root', level='debug')
    h = logging.FileHandler(logfilepath)
    f = logging.Formatter(
        '%(asctime)s %(processName)-10s %(name)s %(levelname)-8s %(message)s')
    h.setFormatter(f)
    root.addHandler(h)


# ------------------------------------------------------------------------------------------------------------------------ #
def worker_configurer(queue):
    """Configures the worker to message the Queue."""
    root = logging.getLogger()
    if len(root.handlers) == 0:
        h = logging.handlers.QueueHandler(queue)
        root.addHandler(h)
        root.setLevel(logging.DEBUG)


# ------------------------------------------------------------------------------------------------------------------------ #
def listener_process(queue, configurer):
    configurer()
    while True:
        try:
            record = queue.get()
            if record is None:  # We send this as a sentinel to tell the listener to quit.
                break
            logger = logging.getLogger(record.name)
            # No level or filter logic applied - just do it!
            logger.handle(record)
        except Exception:
            import sys
            import traceback
            print('Whoops! Problem:', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


# ------------------------------------------------------------------------------------------------------------------------ #
def main_pool(id: str):
    start_time = time.time()

    # Setup basic logging for main process
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Build queue and listener
    queue = mp.Manager().Queue(-1)
    listener = mp.Process(target=listener_process,
                          args=(queue, listener_configurer))
    listener.start()
    logger.info("Listener started")

    # Get the project to execute and assign the worker
    project = ProjectAdmin().get_project(id)
    worker = project.worker
    logger.info("Project {}, id {} received for worker {}".format(
        project.name, project.id, project.worker.__class__.__name__))

    # Execute the project jobs by assigning the work to a process pool to be completed by worker.
    pool = mp.Pool(processes=NUM_PROCESSORS)
    for job in project.jobs:
        pool.apply_async(worker,
                         args=(job, queue, worker_configurer))

    pool.close()
    pool.join()
    queue.put_nowait(None)
    listener.join()
    end_time = time.time()


if __name__ == "__main__":
    mp.freeze_support()
    parser = argparse.ArgumentParser()
    parser.add_argument("id", type=str, help="Project Id to execute.")
    args = parser.parse_args()
    main_pool(args.id)

    # %%
