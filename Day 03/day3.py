#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day3.py
"""
Advent of Code Day 3
https://adventofcode.com/2018/day/3

Copyright David Hoffman, 2018
"""

import pandas as pd
import numpy as np
import scipy.ndimage as ndi
import re


def data():
    """A generator yielding parsed data as slices"""
    with open("input.txt", "r") as file:
        for line in file:
            numbers = re.findall(r"\d+", line)
            left, top, width, height = [int(num) for num in numbers[1:]]
            yield (slice(top, top + height), slice(left, left + width))


if __name__ == "__main__":
    # Part 1
    # Make empty fabric
    fabric = np.zeros((1000, 1000))

    # fill in claims
    for d in data():
        fabric[d] += 1

    # sum any area with more than one claim
    print("Answer 1:", (fabric > 1).sum())

    # Part 2
    # label claims
    lbl, nlbl = ndi.label(fabric)
    lbls = np.arange(1, nlbl + 1)

    # figure out which square inch has more than one claim
    max_values = ndi.labeled_comprehension(fabric, lbl, lbls, np.max, int, 0)

    # find the single area that is not over claimed
    index = np.argwhere(max_values == 1).squeeze()
    good_square = np.argwhere(lbl == index + 1)

    # get the top left corner which will uniquely identify it
    top, left = good_square.min(0)

    # find the number of the claim.
    for i, d in enumerate(data()):
        s0, s1 = d
        top_test = s0.start
        left_test = s1.start
        if top == top_test and left == left_test:
            break

    print("Answer 2:", i + 1)
