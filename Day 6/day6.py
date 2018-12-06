#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day6.py
"""
Advent of Code Day 6
https://adventofcode.com/2018/day/6

Copyright David Hoffman, 2018
"""

import numpy as np
import pandas as pd

# read in data
data = pd.read_csv("input.txt", header=None).values

# calculate max values and make indices
idx = np.indices(data.max(0) + 1)

# calculate distances for all points
distances = abs((idx[None] - data[..., None, None])).sum(1)
mapped = distances.argmin(0)

# any that are equidistant are invalid
mapped[(distances == distances.min(0)).sum(0) > 1] = -1

# calc areas
areas = np.array([(i, (mapped == i).sum()) for i in range(len(data))])

# edges need to be ignored
edges = np.unique(np.concatenate((mapped[[0, -1]].ravel(), mapped[:, [0, -1]].ravel())))
edges = edges[edges > -1]

# filter out areas that correspond to edges
filt = np.ones(len(areas), dtype=bool)
filt[edges] = False
areas_filtered = areas[filt]


if __name__ == '__main__':
    print("Answer 1:", areas_filtered[areas_filtered[:, 1].argmax(), 1])
    print("Answer 2:", (distances.sum(0) < 10000).sum())
