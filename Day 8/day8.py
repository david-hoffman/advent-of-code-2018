#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day8.py
"""
Advent of Code Day 8
https://adventofcode.com/2018/day/8

Copyright David Hoffman, 2018
"""

from collections import deque
import numpy as np
import networkx as nx

data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"


def parse(input_):
    """Parse input data"""
    return deque(int(i) for i in input_.split())


class inc(object):
    """We can use a normal int in a recursive function so make a simple class"""

    def __init__(self, i):
        self.i = i

    def __call__(self, i=1):
        self.i += i


def build_graph(data):
    """build graph from data"""
    # initialize graph
    graph = nx.DiGraph()
    # and incrementor
    node_num = inc(0)

    def build(parent):
        """The recursive function to build the graph"""
        # pull current node number
        node = node_num.i
        # increase node number for next round
        node_num()

        # read header
        # number of children nodes
        num_children = data.popleft()
        # amount of meta data
        num_meta = data.popleft()

        # iterate through children
        for i in range(num_children):
            build(node)
        # after dealing with children if there are any, add the edge and read metadata
        if node:
            graph.add_edge(parent, node)
        graph.nodes[node]['meta'] = tuple(data.popleft() for i in range(num_meta))

    build(node_num.i)

    return graph

if __name__ == '__main__':
    data = parse(data)

    # read real data from file
    # with open("input.txt", "r") as fp:
    #     data = parse(fp.read())

    graph = build_graph(data)

    assert not len(data), "Not all data consumed"
    all_meta = np.concatenate([meta["meta"] for node, meta in graph.nodes.data()])
    print("Answer 1:", all_meta.sum())

    print(graph.nodes.data())
    print(graph[0])
