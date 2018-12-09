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


if __name__ == '__main__':
    data = parse(data)

    with open("input.txt", "r") as fp:
        data = parse(fp.read())

    graph = nx.DiGraph()
    all_meta = []
    all_nodes = [1]

    def build(parent, node):
        # read header
        # number of children nodes
        num_children = data.popleft()
        # amount of meta data
        num_meta = data.popleft()

        print("Data left = {: >3d}, node = {: >3d}, #children = {: >2d}, meta = {: >3d}, total_nodes = {: >3d}".format(len(data), node, num_children, num_meta, len(all_nodes)))
        for i in range(1, num_children + 1):
            build(parent, len(all_nodes))
        # after dealing with children if there are any, add the edge and read metadata
        if node:
            graph.add_edge(parent, node)
            all_nodes.append(1)
        graph.nodes[node]['meta'] = tuple(data.popleft() for i in range(num_meta))
        all_meta.append(graph.nodes[node]['meta'])

    build(0, 0)
    assert not len(data), "Not all data consumed"
    print(graph.nodes.data())
    print(all_meta)
    print(len(all_nodes))
    print(np.concatenate(all_meta).sum())
    all_meta = np.concatenate([meta["meta"] for node, meta in graph.nodes.data()])
    print("Answer 1:", all_meta.sum())
