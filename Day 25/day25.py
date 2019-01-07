#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day25.py
"""
Advent of Code Day 25
https://adventofcode.com/2018/day/25

Copyright David Hoffman, 2018
"""

import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt


def manhattan(pos0, pos1):
    """Calculate manhattan distance between positions"""
    return sum(map(abs, (i - j for i, j in zip(pos0, pos1))))


def parse(input_):
    return [tuple(map(int, line.split()[-1].split(","))) for line in input_.splitlines()]


def find_constellations(points, diagnostics=False, distance=3):
    graph = nx.Graph()
    for pointA, pointB in combinations(points, 2):
        if manhattan(pointA, pointB) <= 3:
            graph.add_edge(pointA, pointB)
        else:
            graph.add_node(pointA)
            graph.add_node(pointB)

    if diagnostics:
        nx.draw(graph)

    return len(list(nx.connected_components(graph)))

test_inputs = []
test_results = []

test_inputs.append("""0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0""")

test_results.append(2)


test_inputs.append("""-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0""")

test_results.append(4)


test_inputs.append("""1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2""")

test_results.append(3)


test_inputs.append("""1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2""")

test_results.append(8)

if __name__ == '__main__':
    for test_result, test_input in zip(test_results, test_inputs):
        assert find_constellations(parse(test_input)) == test_result

    with open("input.txt", "r") as fp:
        print("Answer 1:", find_constellations(parse(fp.read()), diagnostics=True))

    plt.show()
