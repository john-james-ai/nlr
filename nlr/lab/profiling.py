#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \profiling.py                                                                                                 #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Wednesday, November 10th 2021, 5:59:15 am                                                                     #
# Modified : Wednesday, November 10th 2021, 8:52:52 am                                                                     #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
import collections
import time
from pprint import pprint
from datetime import datetime
import psutil
p = psutil.Process()
# print(datetime.now())
X = p.as_dict(attrs=['pid', 'create_time', 'cpu_percent', 'cpu_times', 'num_threads', 'num_handles',
                     'name',    'memory_percent'])

T = ['io_counters', 'memory_full_info', 'num_ctx_switches']
X['resources'] = {
    'num_open_files': len(p.open_files()),
    'num_open_connections': len(p.connections())
}
X['craate_time_format'] = datetime.fromtimestamp(
    p.create_time()).strftime("%Y-%m-%d %H:%M:%S")

final = {}


def flatten(d, prev='', sep='_'):
    items = {}


pprint(X)
final = {}
sep = '_'
for a, b in X.items():
    if isinstance(b, tuple):
        for c, d in b._asdict().items():
            if isinstance(d, tuple):
                for e, f in d._asdict().items():
                    if isinstance(f, tuple):
                        for g, h in f._asdict().items():
                            knu = [a, c, e, g].join(sep)
                            final[knu] = h
                    elif isinstance(f, dict):
                        for g, h in f.items():
                            knu = [a, c, e, g].join(sep)
                            final[knu] = h
                    else:
                        knu = [a, c, e].join(sep)
                        final[knu] = f
            elif isinstance(d, dict):
                for e, f in d.items():
                    if isinstance(f, )
                    for g, h in f.items():
                        knu = [a, c, e, g].join(sep)
                        final[knu] = h

        d2 = v._asdict()

        d3 = {k: v for k, v in d2.items()}
        if isinstance(o, t)
    else:
        final[k] = v
pprint(final)
print(len(p.open_files()))
print(len(p.connections()))
print(p.name())
print(datetime.fromtimestamp(
    p.create_time()).strftime("%Y-%m-%d %H:%M:%S"))


def flatten(d, parent_key='', sep='_'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, tuple):
                items.extend(flatten(v, new_key, sep=sep))
            else:
                items.append((new_key, v))
        return dict(items)
    elif isinstance(d, tuple):


print(flatten(X))
# %%
