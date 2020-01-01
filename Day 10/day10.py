#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day10.py
"""
Advent of Code Day 10
https://adventofcode.com/2018/day/10

Copyright David Hoffman, 2018
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import count
import re

test_data = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


def bounding_box(arr):
    """return area of bounding box of point cloud"""
    return np.prod(arr.max(0) - arr.min(0))


if __name__ == "__main__":
    data = test_data

    with open("input.txt", "r") as fp:
        data = fp.read()

    # read in all data as a flat array
    pos_vel = np.array(list(map(int, re.findall(r"-?\d+", data))))
    # reshape and extract positions and velocities
    pos_vel = pos_vel.reshape(-1, 2, 2)
    pos = pos_vel[:, 0, ::-1]
    vel = pos_vel[:, 1, ::-1]

    # now we assume that the bounding box monotonically decreases as we approach
    # the message, so iterate through times, calculating the bounding box
    # as soon as the difference is negative, break and the previous value is the
    # correct one

    # initialize area
    old_box = np.inf
    for t in count():
        # position at time t
        new_pos = pos + t * vel
        # bounding box area at time t
        new_box = bounding_box(new_pos)
        # has it gotten bigger?
        if old_box - new_box < 0:
            break
        old_box = new_box

    # best time is one previous
    best_t = t - 1

    print("best time:", best_t, "(s)")

    # show the message
    new_pos = pos + best_t * vel
    # message is flipped vertically
    plt.scatter(new_pos[:, 1], -new_pos[:, 0])
    plt.gca().set_aspect(1)
    plt.show()
