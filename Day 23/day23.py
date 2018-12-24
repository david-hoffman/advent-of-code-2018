#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day23.py
"""
Advent of Code Day 23
https://adventofcode.com/2018/day/23

Copyright David Hoffman, 2018
"""

import numpy as np
import tqdm
import matplotlib.pyplot as plt
from itertools import product
import re
re_digits = re.compile(r"-?\d+")


def strip_digits(input_):
    """Strip numbers from a string"""
    return list(map(int, re_digits.findall(input_)))


def parse(input_):
    """parse input"""
    arr = np.array(strip_digits(input_))
    arr.shape = (-1, 4)
    pos = arr[:, :3]
    radius = arr[:, -1]
    return pos, radius


def ranges(a_pos, pos):
    return abs(pos - a_pos).sum(1)


def inrange(a_pos, pos, radii):
    return (ranges(a_pos, pos) <= radii).sum()


def find_best_points(p, r, num_steps=25, search_radius=1):
    """For part II its all about restricting the search space

    We only need to search along the 3 cardinal directions from each bot and only up to each bot's signal
    radius (because of manhattan distance). We can find the best such point along each direction with a
    naive maximization search algorithm assuming that the function is not too rough. Then we have three such
    points for each bot which we can easily find the maximum count and minimum distance.
    """
    directions = np.array((
        (1, 0, 0),
        (0, 1, 0),
        (0, 0, 1)
    ))
    
    for direction in directions:
        start = -r
        stop = r
        # plt.figure()
        while True:
            step = max((stop - start) // num_steps, 1)
            test_points = np.arange(start, stop + step, step)
            counts = np.array([inrange(p + direction * i, pos, radii) for i in test_points])
            idx_max = counts.argmax()
            # print(counts.shape, idx_max, test_points[idx_max], p + direction * test_points[idx_max], counts[idx_max], step)
            # plt.plot(test_points, counts)
            start = test_points[max(idx_max - search_radius, 0)]
            stop = test_points[min(idx_max + search_radius, len(test_points) - 1)]
            if step == 1:
                break
        # plt.plot(test_points[idx_max], counts[idx_max], "ro")
        # plt.show()
        yield abs(p + direction * test_points[idx_max]).sum(), counts[idx_max]

test_input0 = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1"""

test_input1 = """pos=<10,12,12>, r=2
pos=<12,14,12>, r=2
pos=<16,12,12>, r=4
pos=<14,14,14>, r=6
pos=<50,50,50>, r=200
pos=<10,10,10>, r=5"""


if __name__ == '__main__':
    pos, radii = parse(test_input1)

    with open("input.txt", "r") as fp:
        pos, radii = parse(fp.read())

    print("Answer 1:", inrange(pos[radii.argmax()], pos, radii.max()))

    all_points = []
    for p, r in zip(tqdm.tqdm(pos), radii):
        all_points.extend(list(find_best_points(p, r + 1)))

    # print(all_points)
    # sort by descending counts first and ascending distance second
    all_points2 = sorted(all_points, key=lambda x: (-x[1], x[0]))
    print("Answer 2:", all_points2[0])
