#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \flatten.py                                                                                                   #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Wednesday, November 10th 2021, 8:54:32 am                                                                     #
# Modified : Wednesday, November 10th 2021, 9:28:47 am                                                                     #
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
X = p.as_dict(attrs=['name', 'pid', 'create_time', 'cpu_percent', 'num_threads', 'num_handles',
                     'memory_percent'])

print(X)
T = [p.io_counters(), p.memory_full_info(), p.num_ctx_switches(), p.cpu_times()]
X['resources'] = {
    'num_open_files': len(p.open_files()),
    'num_open_connections': len(p.connections())
}
X['craate_time_format'] = datetime.fromtimestamp(
    p.create_time()).strftime("%Y-%m-%d %H:%M:%S")

final = {}
# print(X)
for t in T:
    for k, v in t._asdict().items():
        X[k] = v
print(X.keys())
pprint(X)

# %%
