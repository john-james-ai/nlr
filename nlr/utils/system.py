#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \system.py                                                                                                    #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Wednesday, November 10th 2021, 9:10:56 am                                                                     #
# Modified : Wednesday, November 10th 2021, 11:19:29 am                                                                    #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
from pprint import pprint
from datetime import datetime
import psutil
import pandas as pd
pd.options.display.max_columns = 100

# ------------------------------------------------------------------------------------------------------------------------ #
profile_template_filepath = "./nlr/utils/profiling.csv"


class Profiler:
    """Captures process resource utilization statistics."""

    def __init__(self, jobname: str) -> None:
        self.jobname = jobname
        self.profiler = psutil.Process()
        self._profile_template = pd.read_csv(profile_template_filepath)
        self._stats = {}

    def extract_tuple(self) -> dict:
        d = {}
        T = [self.profiler.io_counters(), self.profiler.memory_full_info(),
             self.profiler.num_ctx_switches(), self.profiler.cpu_times()]
        for t in T:
            for k, v in t._asdict().items():
                d[k] = v
        return d

    def extract_dict(self) -> dict:

        d = self.profiler.as_dict(attrs=['name', 'pid', 'create_time', 'cpu_percent', 'num_threads', 'num_handles',
                                         'memory_percent'])
        d['num_open_files'] = len(self.profiler.open_files())
        d['num_connections'] = len(self.profiler.connections())
        d['create_time_format'] = datetime.fromtimestamp(
            self.profiler.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        d['job'] = self.jobname
        return d

    def select(self) -> dict:
        stats = self._profile_template['stat'].values
        d = {}
        for stat in stats:
            d[stat] = self._stats[stat]
        return d

    def format(self, d: dict) -> None:
        data = {}
        data['stat'] = d.keys()
        data['value'] = d.values()
        df = pd.DataFrame(data=data)
        self.profile = self._profile_template.merge(
            right=df, left_on='stat', right_on='stat', how='left')

    def start(self) -> None:
        self._stats['start_time'] = datetime.now()

    def end(self) -> None:
        self._stats['end_time'] = datetime.now()
        self._stats['wall_time'] = self._stats['end_time'] -\
            self._stats['start_time']
        d = self.extract_dict()
        self._stats.update(d)
        d = self.extract_tuple()
        self._stats.update(d)
        d = self.select()
        self.format(d)


if __name__ == '__main__':
    p = Profiler('job')
    p.start()
    p.end()
    # %%
