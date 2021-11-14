#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# ======================================================================================================================== #
# Project  : Natural Language Recommendation                                                                               #
# Version  : 0.1.0                                                                                                         #
# File     : \tuples.py                                                                                                    #
# Language : Python 3.7.11                                                                                                 #
# ------------------------------------------------------------------------------------------------------------------------ #
# Author   : John James                                                                                                    #
# Company  : nov8.ai                                                                                                       #
# Email    : john.james.sf@gmail.com                                                                                       #
# URL      : https://github.com/john-james-sf/nlr                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# Created  : Saturday, November 13th 2021, 8:03:33 am                                                                      #
# Modified : Saturday, November 13th 2021, 8:16:10 am                                                                      #
# Modifier : John James (john.james.sf@gmail.com)                                                                          #
# ------------------------------------------------------------------------------------------------------------------------ #
# License  : BSD 3-clause "New" or "Revised" License                                                                       #
# Copyright: (c) 2021 nov8.ai                                                                                              #
# ======================================================================================================================== #
# %%
l = []
for i in range(5):
    d = {}
    for j in range(5):
        key = 'key_' + str(i) + '_' + str(j)
        value = 'value_' + str(i) + '_' + str(j)
        d[key] = value
    l.append(d)

tuples = []
for row in l:
    t = tuple(v for v in row.values())
    tuples.append(t)
print(tuples)
# %%
