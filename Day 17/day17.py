#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day17.py
"""
Advent of Code Day 17
https://adventofcode.com/2018/day/17

Copyright David Hoffman, 2018
"""

import numpy as np
import tqdm


# water can't go up so no up direction
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

DIRECTIONS = LEFT, RIGHT, DOWN


def place_water(map_, water, char):
    """"""
    new_map = map_.copy()
    if water:
        y, x = np.array(tuple(water)).T
        new_map[y, x] = char
    return new_map


def parse(input_):
    """Parse input into units and map with map characters fixed"""
    slices = []
    for line in input_:
        first, second = line.split(", ")
        order = first[0] == "y"
        first = int(first[2:])
        start, stop = list(map(int, second[2:].split("..")))
        second = slice(start, stop + 1)
        if order:
            slices.append((first, second))
        else:
            slices.append((second, first))

    # find maxes
    maxy, maxx = 0, 0
    miny, minx = np.inf, np.inf
    for y, x in slices:
        if isinstance(y, slice):
            maxy = max(maxy, y.stop)
            maxx = max(maxx, x + 1)

            miny = min(miny, y.start)
            minx = min(minx, x)
        else:
            maxy = max(maxy, y + 1)
            maxx = max(maxx, x.stop)

            miny = min(miny, y)
            minx = min(minx, x.start)

    map_ = np.full((maxy, maxx), ".")

    for y, x in slices:
        map_[y, x] = "#"

    # spring at 0, 500
    # map_[0, 500] = "+"
    # make map_ immutable
    map_.flags.writeable = False
    return map_, (maxy, maxx), (miny, minx)


def new_vertex(old_vertex, direction):
    return tuple(i + di for i, di in zip(old_vertex, direction))


def fill_water(start, map_,):
    """this is essentially a depth first search"""
    visited = set()
    standing = set()
    stack = [(start, DOWN)]

    def _test_char(vertex, test_char):
        if vertex in visited:
            return False
        try:
            char = map_[vertex]
        except IndexError:
            # end of map
            return False
        return char == test_char

    def empty(vertex):
        return _test_char(vertex, ".")

    def clay(vertex):
        return _test_char(vertex, "#")

    def search1d(vertex, direction):
        to_fill = set()
        while vertex in visited:
            to_fill.add(vertex)
            vertex = new_vertex(vertex, direction)
        return to_fill, clay(vertex)

    def update(ylevel):
        """Update which water is standing and which is flowing"""
        # first update standing
        for vertex in filter(lambda x: x[0] == ylevel, visited):
            if vertex in standing:
                continue
            left_set, left_end = search1d(vertex, LEFT)
            right_set, right_end = search1d(vertex, RIGHT)
            if left_end and right_end:
                standing.update(left_set, right_set)

    def flowable(vertex):
        """Check lower right and lower left for clay"""
        return any(clay(new_vertex(vertex, direction)) for direction in (LEFT, RIGHT)) and vertex not in visited

    while stack:
        vertex, old_dir = stack.pop()
        if vertex in visited:
            # if we've been here before move along
            continue
        if clay(vertex) or not empty(vertex):
            # if we've hit clay or moved off map
            continue
        if old_dir is not DOWN:
            update(vertex[0] + 1)
            down = new_vertex(vertex, DOWN)
            if not clay(down) and down not in standing and not flowable(down):
                # we've moved sideways and we're over thin air, but not flowable
                continue

        visited.add(vertex)
        for direction in DIRECTIONS:
            stack.append((new_vertex(vertex, direction), direction))
        yield visited, standing, vertex


test_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


if __name__ == '__main__':
    map_, maxes, mins = parse(test_input.splitlines())
    print("\n".join("".join(line) for line in map_[:, 494:]))
    for i, (water, standing, current) in enumerate(fill_water((0, 500), map_)):
        print()
        new_map = place_water(map_, water, "|")
        new_map = place_water(new_map, standing, "~")
        new_map = place_water(new_map, current, "*")
        print("\n".join("".join(line) for line in new_map[:, 494:]))
        # if i > 57:
        #     break
    
    print("+" * 80)
    new_map = place_water(map_, water, "|")
    new_map = place_water(new_map, standing, "~")
    print("\n".join("".join(line) for line in new_map[:, 494:]))

    print(len(list(filter(lambda x: x[0] >= mins[0], water))))

    with open("input.txt", "r") as fp:
        map_, maxes, mins = parse(fp.readlines())

    print(map_.shape)

    for i, (water, standing, current) in enumerate((fill_water((0, 500), map_))):
        if not i % 250:
            print(len(water), len(standing))
            new_map = place_water(map_, water, "|")
            new_map = place_water(new_map, standing, "~")
            new_map = place_water(new_map, current, "*")
            y, x = current
            print("\n".join("".join(line) for line in new_map[y - 20: y + 20, x - 20:x + 20]))

    print(len(list(filter(lambda x: x[0] >= mins[0], water))))