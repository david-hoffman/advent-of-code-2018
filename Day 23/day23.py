#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day23.py
"""
Advent of Code Day 23
https://adventofcode.com/2018/day/23

Copyright David Hoffman, 2018
"""

import numpy as np
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


def get_octants(min_radius, max_radius):
    for octant in product((1, 3), (1, 3), (1, 3)):
        yield (max_radius - min_radius) * octant // 4 + min_radius


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

    print(inrange(pos[radii.argmax()], pos, radii))

    # do a binary search in 3D, there's 8 octants for each iteration
    max_radius = pos.max(0)
    min_radius = pos.min(0)
    # print([octant for octant in get_octants(min_radius, max_radius)])
    # print((max_radius - min_radius) / max_radius.max())

    n_range = np.array([inrange(p, pos, radii) for p in pos])
    search_points = list(zip(map(tuple, pos), n_range))

    def find_next_in_range(p, pos, radii):
        """Find the point that moving the shortest distance will bring it in range"""
        n_inrange = inrange(p, pos, radii)
        vectors = (pos - p)
        mags = abs(vectors).sum(1)
        to_move = mags - radii
        next_idx = to_move.argsort()[n_inrange]
        return pos[next_idx], radii[next_idx]

    # best_points = [(p, inrange(p, pos, radii)) for p in search_points]
    # best_num = max(num for p, num in best_points)
    points_seen = set(search_points)
    while search_points:
        p, old_n = search_points.pop()
        p_next, r_next = find_next_in_range(p, pos, radii)
        v_move = (p_next - p)
        v_mag = abs(v_move).sum() 
        v_move = (v_move * (v_mag - r_next) / v_mag).round().astype(int)
        p_new = tuple(p + v_move)
        num_new = inrange(p_new, pos, radii)
        if num_new >= old_n and (p_new, num_new) not in points_seen:
            best_num = num_new
            search_points.append((p_new, num_new))
        points_seen.add((p_new, num_new))
        print(len(search_points), p, old_n)

    arr = np.array([(np.abs(pos).sum(), num) for pos, num in points_seen])

    print(arr[arr[:, 1].argmax()])
