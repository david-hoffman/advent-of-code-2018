#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day17.py
"""
Advent of Code Day 17
https://adventofcode.com/2018/day/17

Copyright David Hoffman, 2018
"""

import numpy as np


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
    ny, nx = 0, 0
    for y, x in slices:
        if isinstance(y, slice):
            ny = max(ny, y.stop)
            nx = max(nx, x + 1)
        else:
            ny = max(ny, y + 1)
            nx = max(nx, x.stop)

    map_ = np.full((ny, nx), ".")

    for y, x in slices:
        map_[y, x] = "#"

    # spring at 0, 500
    # map_[0, 500] = "+"
    # make map_ immutable
    map_.flags.writeable = False
    return map_


def fill_water(start, map_, visited=None, settled=None):
    """this is essentially a depth first search"""
    if visited is None:
        visited = set()
    if settled is None:
        settled = set()
    stack = [(start, DOWN)]

    def empty(vertex):
        if vertex in visited:
            return False
        try:
            char = map_[vertex]
        except IndexError:
            # end of map
            return False
        return char == "."

    def clay(vertex):
        if vertex in visited:
            return False
        try:
            char = map_[vertex]
        except IndexError:
            # end of map
            return False
        return char == "#"

    def flowable(vertex):
        if vertex in visited:
            return False
        l = []
        # check lower left and lower right, if any are clay we can flow
        for direction in (LEFT, RIGHT):
            new_vertex = tuple(np.add(vertex, direction))
            l.append(clay(new_vertex) and new_vertex not in visited)
        if any(l):
            return True
        return False

    def flowing(vertex):
        if vertex in settled:
            return True
        l = []
        flowing = []
        for direction in DIRECTIONS:
            new_vertex = tuple(np.add(vertex, direction))
            if clay(new_vertex) or new_vertex in settled:
                l.append(True)
            else:
                l.append(False)
        if l[-1] and any(l[:2]):
            settled.add(vertex)
            return True
        return False

    def is_settled(vertex):
        if vertex in settled:
            return True
        l = []
        flowing = []
        for direction in DIRECTIONS:
            new_vertex = tuple(np.add(vertex, direction))
            if clay(new_vertex) or new_vertex in settled:
                l.append(True)
            else:
                l.append(False)
        if l[-1] and any(l[:2]):
            settled.add(vertex)
            return True
        return False

    def surrounded1(vertex):
        left = tuple(np.add(vertex, LEFT))
        right = tuple(np.add(vertex, RIGHT))
        return settled.issuperset((vertex, left, right))

    def surrounded2(vertex):
        left = tuple(np.add(vertex, LEFT))
        left = tuple(np.add(left, LEFT))
        right = tuple(np.add(vertex, RIGHT))
        right = tuple(np.add(right, RIGHT))
        flowing = (visited - settled)
        return left in flowing or right in flowing

    while stack:
        vertex, old_dir = stack.pop()
        for v in visited:
            is_settled(v)
        if not empty(vertex) or vertex in visited:
            # we hit a water or clay
            continue
        if old_dir is not DOWN:
            # need to check if we've moved over nothing
            print(vertex, surrounded2(vertex))
            down = tuple(np.add(vertex, DOWN))
            if empty(down) and not flowable(down):
                continue
            if not is_settled(vertex) and not clay(down) and not surrounded1(down) and not surrounded2(vertex):
                continue
        visited.add(vertex)
        for direction in DIRECTIONS:
            stack.append((tuple(np.add(vertex, direction)), direction))
        yield visited, settled, vertex


test_input = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""


if __name__ == '__main__':
    map_ = parse(test_input.splitlines())
    print("\n".join("".join(line) for line in map_[:, 494:]))
    for water, settled, current in fill_water((0, 500), map_):
        print()
        new_map = place_water(map_, water, "|")
        new_map = place_water(new_map, settled, "~")
        new_map = place_water(new_map, current, "*")
        print("\n".join("".join(line) for line in new_map[:, 494:]))
    
    print("+" * 80)
    new_map = place_water(map_, water, "|")
    new_map = place_water(new_map, settled, "~")
    print("\n".join("".join(line) for line in new_map[:, 494:]))
