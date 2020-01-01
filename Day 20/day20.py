#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day20.py
"""
Advent of Code Day 20
https://adventofcode.com/2018/day/20

Copyright David Hoffman, 2018
"""

from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

DIRECTIONS = dict(E=(0, 1), W=(0, -1), N=(-1, 0), S=(1, 0))


def sum_tuple(t0, t1):
    return tuple(i + j for i, j in zip(t0, t1))


def build_graph(input_):
    instructions = input_[1:-1]
    branch_stack = []
    growing_ends = {(0, 0)}
    graph = nx.Graph()

    for char in instructions:
        if char == "(":
            # start branch
            # what's the index where the branch starts?
            branch_stack.append(growing_ends)
            continue
        elif char == ")":
            # branch end, restart from stack
            growing_ends = growing_ends | branch_stack.pop()
        elif char == "|":
            # branch
            growing_ends = branch_stack[-1]
        else:
            new_edges = [
                (end, sum_tuple(end, DIRECTIONS[char])) for end in growing_ends
            ]
            graph.add_edges_from(new_edges)
            # update growing ends
            growing_ends = {new for old, new in new_edges}

    return graph


def long_short_path(graph):
    path_lengths = nx.shortest_path_length(graph, (0, 0))
    return max(path_lengths.values())


tests = (
    ("^WNE$", 3),
    ("^ENWWW(NEEE|SSE(EE|N))$", 10),
    ("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$", 18),
    ("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$", 23),
    ("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$", 31),
)

if __name__ == "__main__":

    for test, result in tests:
        graph = build_graph(test)
        test_result = long_short_path(graph)
        assert test_result == result, "{} != {}".format(test_result, test)

    with open("input.txt", "r") as fp:
        graph = build_graph(fp.read().strip())

    result = long_short_path(graph)
    print("Answer 1:", result)

    path_lengths = nx.shortest_path_length(graph, (0, 0))
    print("Answer 2:", sum(length >= 1000 for length in path_lengths.values()))

    nx.draw_spectral(graph)
    plt.gcf().savefig("test.pdf")

    # maze = nx.Graph()

    # paths = open('input.txt').read()[1:-1]

    # pos = {0}  # the current positions that we're building on
    # stack = []  # a stack keeping track of (starts, ends) for groups
    # starts, ends = {0}, set()  # current possible starting and ending positions

    # for c in paths:
    #     if c == '|':
    #         # an alternate: update possible ending points, and restart the group
    #         ends.update(pos)
    #         pos = starts
    #     elif c in 'NESW':
    #         # move in a given direction: add all edges and update our current positions
    #         direction = {'N': 1, 'E': 1j, 'S': -1, 'W': -1j}[c]
    #         maze.add_edges_from((p, p + direction) for p in pos)
    #         pos = {p + direction for p in pos}
    #     elif c == '(':
    #         # start of group: add current positions as start of a new group
    #         stack.append((starts, ends))
    #         starts, ends = pos, set()
    #     elif c == ')':
    #         # end of group: finish current group, add current positions as possible ends
    #         pos.update(ends)
    #         starts, ends = stack.pop()

    # # find the shortest path lengths from the starting room to all other rooms
    # lengths = nx.algorithms.shortest_path_length(maze, 0)

    # print('part1:', max(lengths.values()))
    # print('part2:', sum(1 for length in lengths.values() if length >= 1000))
