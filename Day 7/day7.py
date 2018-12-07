#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day7.py
"""
Advent of Code Day 7
https://adventofcode.com/2018/day/7

Copyright David Hoffman, 2018
"""

import string
import numpy as np
import scipy.ndimage as ndi

"""
This seems to be a simple sorting algorithm. Start with alphabet in order
Then swap characters as needed
"""

# data = """Step C must be finished before step A can begin.
# Step C must be finished before step F can begin.
# Step A must be finished before step B can begin.
# Step A must be finished before step D can begin.
# Step B must be finished before step E can begin.
# Step D must be finished before step E can begin.
# Step F must be finished before step E can begin."""

steps = np.array([char for char in string.ascii_uppercase])


def parse(line):
    return np.array((line[5], line[36]))


def sort_steps(instructions, steps):
    not_moved = np.zeros(len(steps))
    for line in instructions:
        first, last = parse(line)
        first_idx = np.argwhere(steps == first).squeeze()
        last_idx = np.argwhere(steps == last).squeeze()

        if first_idx > last_idx:
            steps[first_idx], steps[last_idx] = steps[last_idx], steps[first_idx]
        else:
            not_moved[np.array((first_idx, last_idx))] += 1

    same = np.diff(not_moved) == 0
    same = np.concatenate(((False,), same))
    same[np.argwhere(same == 1) - 1] = True
    lbls, num_lbl = ndi.label(same)

    for lbl in range(1, num_lbl + 1):
        to_sort = lbls == lbl
        steps[to_sort] = np.sort(steps[to_sort])
    print(not_moved)


if __name__ == '__main__':
    with open("input.txt", "r") as fp:
        data = "".join(fp.readlines())

    data = data.strip("\n").split("\n")

    print("".join(steps))
    steps_old = np.zeros_like(steps)
    while not np.array_equal(steps, steps_old):
        steps_old = steps.copy()
        sort_steps(data, steps)
        print("".join(steps))

