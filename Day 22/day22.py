#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day22.py
"""
Advent of Code Day 22
https://adventofcode.com/2018/day/22

Copyright David Hoffman, 2018
"""

import numpy as np

translation = str.maketrans("012", ".=|")

np.seterr(over="warn", under="warn")

Y = 16807
X = 48271
errosion_m = 20183
modulo = 20183


def parse(input_):
    depth, target = input_.splitlines()
    depth = int(depth.split()[-1])
    target = list(map(int, (i for i in target.split()[-1].split(","))))
    return depth, target[::-1]

test_input = """depth: 510
target: 10,10"""

if __name__ == '__main__':
    depth, target = parse(test_input)

    with open("input.txt", "r") as fp:
        depth, target = parse(fp.read())
    map_ = np.zeros(np.add(1, target), dtype=int)
    # fill in y = 0
    map_[0, :] = np.arange(map_.shape[1]) * Y
    # fill in x = 0
    map_[:, 0] = np.arange(map_.shape[0]) * X
    # throw away useless bit
    map_ %= modulo
    # fill in the rest
    for i in range(1, map_.shape[0]):
        for j in range(1, map_.shape[1]):
            # need to add depth here so that we can get erosion level
            map_[i, j] = ((map_[i - 1, j] + depth) * (map_[i, j - 1] + depth)) % modulo
    # target is zer0
    map_[-1, -1] = 0
    # covert map to type
    map_ = (map_ + depth) % modulo
    map_ %= 3
    # print("\n".join("".join(map(str, line)) for line in map_).translate(translation))
    print("Answer 1:", map_.sum())

    