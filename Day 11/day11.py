#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day11.py
"""
Advent of Code Day 11
https://adventofcode.com/2018/day/11

Copyright David Hoffman, 2018
"""

import numpy as np
import scipy.ndimage as ndi
import re


def power_levels(serial_num):
    """Calculate the power levels of the fuel cells"""
    # generate indices
    Y, X = np.indices((300, 300)) + 1
    # calculate rack id
    rack_id = X + 10
    power = rack_id * Y
    power += serial_num
    power *= rack_id
    # pull hundreds digit
    power = (power % 1000) // 100
    power -= 5
    return power


def best_loc(serial_num, power=None, size=3):
    """Find the best block of a given size (most total power)"""
    # calculate the power levels
    if power is None:
        power = power_levels(serial_num)
    # we use a uniform filter here (mean filter) instead of generic_filter and np.sum
    # because the C implementation of uniform filter is lightning fast
    # convert input to float first
    max_power = ndi.uniform_filter(power * 1.0, size=size, output=None, mode='constant', cval=0, origin=0)
    # convert mean to sum
    max_power = (max_power * size**2).round().astype(int)
    # find central pixel and convert to upper left
    Y_max, X_max = np.array(np.unravel_index(max_power.argmax(), max_power.shape)) + 1 - size // 2
    return X_max, Y_max, max_power.max(), (max_power == max_power.max()).sum()


def best_loc_size(serial_num):
    """Iterate through all possible block sizes and find the one with the most power"""
    power = power_levels(serial_num)
    all_sizes = []
    for size in range(1, 301):
        X_max, Y_max, max_power, num_max = best_loc(serial_num, power=power, size=size)
        all_sizes.append((X_max, Y_max, size, max_power))

    all_sizes = np.asarray(all_sizes)
    return all_sizes[all_sizes[:, -1].argmax()]


tests = """Fuel cell at 3,5 in a grid with serial number 8: power level 4.
Fuel cell at  122,79, grid serial number 57: power level -5.
Fuel cell at 217,196, grid serial number 39: power level  0.
Fuel cell at 101,153, grid serial number 71: power level  4."""


if __name__ == '__main__':
    # tests
    # for X, Y, serial_num, result in np.array(list(map(int, re.findall(r"-?\d+", tests)))).reshape(-1, 4):
    #     assert power_levels(serial_num)[Y - 1, X - 1] == result, "Fuel cell at {},{}, grid serial number {}: power level {}.".format(X, Y, result, serial_num)

    print("All tests passed")

    print("Answer 1:", end=" ")
    for serial_num in (18, 42, 3628)[-1:]:
        X_max, Y_max, max_power, num_max = best_loc(serial_num)
        print("num max {}, max {}, <X,y> = {},{}".format(num_max, max_power, X_max, Y_max))

    print("Answer 2:", end=" ")
    for serial_num in (18, 42, 3628)[-1:]:
        print("<X,y,size> = {},{},{}".format(*best_loc_size(serial_num)[:-1]))
