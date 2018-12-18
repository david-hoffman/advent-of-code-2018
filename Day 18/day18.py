#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day18.py
"""
Advent of Code Day 18
https://adventofcode.com/2018/day/18

Copyright David Hoffman, 2018
"""

import numpy as np


def parse(input_):
    """Convert text to array"""
    return np.array([np.array([char for char in line]) for line in input_])


def neighborhood(vertex, map_, half_kernel_size=1):
    """Pull neighborhood around point"""
    s = tuple(slice(y - half_kernel_size, y + half_kernel_size + 1) for y in vertex)
    values = map_[s].ravel()
    center = values.size // 2
    assert values[center] == map_[vertex]
    values = np.delete(values, center)
    return map_[vertex], values


def new_square(center, neighbors):
    """Update current location based on problem rules"""
    if center == ".":
        # An open acre will become filled with trees if three or more adjacent acres contained trees.
        # Otherwise, nothing happens.
        if (neighbors == "|").sum() >= 3:
            return "|"
    elif center == "|":
        # An acre filled with trees will become a lumberyard if three or more adjacent acres were lumberyards.
        # Otherwise, nothing happens.
        if (neighbors == "#").sum() >= 3:
            return "#"
    elif center == "#":
        # An acre containing a lumberyard will remain a lumberyard if it was adjacent to at least one other lumberyard
        # and at least one acre containing trees. Otherwise, it becomes open.
        if not ((neighbors == "#").any() and (neighbors == "|").any()):
            return "."
    else:
        raise RuntimeError(center)
    return center


def map_to_str(map_):
    """From array to string"""
    return "\n".join("".join(line) for line in map_)


def update(map_):
    """Update all locations on map"""
    # pad map out to be able to calculate edges
    padded_map = np.pad(map_, (1, 1), "constant", constant_values=".")
    ny, nx = map_.shape
    new_map = map_.copy()
    # iterate through tiles updating
    for i in range(ny):
        for j in range(nx):
            new_map[i, j] = new_square(*neighborhood((i + 1, j + 1), padded_map))

    return new_map


def result(map_):
    """Multiplying the number of wooded acres by the number of lumberyards gives the total resource value"""
    wooded = (map_ == "|").sum()
    lumberyards = (map_ == "#").sum()
    return wooded * lumberyards


def detect_pattern(series):
    """There has to be a pattern, right???"""
    for i in range(1, len(series) // 2 + 1):
        one = series[-i:]
        two = series[-2 * i:-i]
        if one == two:
            return series[:-2 * i], one, two

test_input = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

test_result = """.||##.....
||###.....
||##......
|##.....##
|##.....##
|##....##|
||##.####|
||#####|||
||||#|||||
||||||||||"""

if __name__ == '__main__':
    map_ = parse(test_input.splitlines())
    # print(map_to_str(map_))
    for i in range(10):
        # print()
        map_ = update(map_)
        # print(map_to_str(map_))

    assert map_to_str(map_) == test_result
    assert result(map_) == 1147

    with open("input.txt", "r") as fp:
        map_ = original_map = parse(fp.read().splitlines())

    # print(map_to_str(map_))
    for i in range(10):
        # print()
        map_ = update(map_)
        # print(map_to_str(map_))

    print("Answer 1:", result(map_))

    map_ = original_map

    # print(map_to_str(map_))
    series = []
    rounds = 1000000000
    for i in range(rounds):
        series.append(result(map_))
        pattern = detect_pattern(series)
        # print(series[-1])
        if pattern:
            # if a pattern has formed stop!
            break
        map_ = update(map_)
        # print(map_to_str(map_))

    # extrapolate pattern to end
    print("Answer 2:", pattern[1][(rounds - len(pattern[0])) % len(pattern[1])])
