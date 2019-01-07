#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day22.py
"""
Advent of Code Day 22
https://adventofcode.com/2018/day/22

Copyright David Hoffman, 2018
"""

import numpy as np
import networkx as nx

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
    print("\n".join("".join(map(str, line)) for line in map_).translate(translation))
    print("Answer 1:", map_.sum())

    # reddit answer
    from heapq import heappush, heappop

    with open('input.txt', 'r') as f:
        depth = int(next(f).split()[-1])
        target = complex(*map(int, next(f).split()[-1].split(',')))

    ROCKY, WET, NARROW = 0, 1, 2
    NEITHER, TORCH, CLIMB = 0, 1, 2
    m_erosion = dict()
    m_geo_index = dict()

    def viz(max):
        m_viz_erosion = {ROCKY: '.', WET: '=', NARROW: '|'}

        for y in range(int(max.imag) + 1):
            for x in range(int(max.real) + 1):
                pos = x + 1j * y
                if pos == 0:
                    print('M', end='')
                elif pos == target:
                    print('T', end='')
                else:
                    print(m_viz_erosion[erosion(pos) % 3], end='')
            print()


    def erosion(p):
        if p in m_erosion:
            return m_erosion[p]
        ret = (geo_index(p) + depth) % 20183
        m_erosion[p] = ret
        return ret


    def geo_index(p):
        if p in m_geo_index:
            return m_geo_index[p]

        if p == 0 or p == target:
            ret = 0
        elif p.imag == 0:
            ret = p.real * 16807
        elif p.real == 0:
            ret = p.imag * 48271
        else:
            ret = erosion(p - 1) * erosion(p - 1j)

        m_geo_index[p] = ret
        return ret

    # Part 1
    risk = 0
    for y in range(int(target.imag) + 1):
        for x in range(int(target.real) + 1):
            risk += erosion(x + 1j * y) % 3
    print('Part 1:', int(risk))

    # Part 2
    # Do a BFS search with a priority queue.
    heap = [(0, 0, 0, TORCH)]  # (time, x, y, equipment), heap sorted by time, so time has to be first
    visited = {(0, TORCH): 0}  # (pos, equipment): time

    def visit_next(time, pos, eq, heap):
        for newpos in [pos + 1, pos - 1, pos + 1j, pos - 1j]:
            if newpos.real < 0 or newpos.imag < 0:  # out of bounds
                continue
            if erosion(newpos) % 3 == eq:  # can we go here with this equipment?
                continue
            if (newpos, eq) in visited and visited[(newpos, eq)] <= time:  # there is a faster way
                continue
            visited[(newpos, eq)] = time
            heappush(heap, (time, newpos.real, newpos.imag, eq))

    while True:
        # It's annoying we cannot use the heap with complex numbers because they cannot be ordered...
        time, x, y, eq = heappop(heap)
        pos = x + 1j * y
        if (pos, eq) == (target, TORCH):
            break

        # Try to go to the next square with the same equipment
        time += 1
        visit_next(time, pos, eq, heap)

        # Try to go to the next square with alternative equipment
        # The region's type and the two allowed equipments always sum to 3
        # because of the way we defined them
        time += 7
        eq = 3 - eq - erosion(pos) % 3
        visit_next(time, pos, eq, heap)

    print('Part 2:', time)
