#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day7.py
"""
Advent of Code Day 7
https://adventofcode.com/2018/day/7

Copyright David Hoffman, 2018
"""

import string
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

"""
This seems to be a simple sorting algorithm. Start with alphabet in order
Then swap characters as needed
"""

data = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin."""


def parse(line):
    return line[5], line[36]


if __name__ == '__main__':
    with open("input.txt", "r") as fp:
        data = "".join(fp.readlines())

    data = data.strip("\n").split("\n")
    graph = nx.DiGraph()

    edges = sorted([parse(line) for line in data], key=lambda x: x[0])
    graph.add_edges_from(edges)

    # clean_graph = nx.transitive_reduction(graph)

    ans = "".join(nx.dfs_postorder_nodes(graph.reverse()))
    print("Answer 1:", ans)

    # Build task tree
    task_tree = dict()
    all_steps = set()
    for line in data:
        parent, child = parse(line)
        print("{} ---> {}".format(parent, child))
        all_steps.add(parent)
        all_steps.add(child)
        try:
            task_tree[parent].add(child)
        except KeyError:
            task_tree[parent] = {child}

    # print(task_tree, all_steps)

    # Clear out last steps, i.e parent's with no children
    steps_reversed = steps_to_process = sorted(all_steps.symmetric_difference(task_tree))[::-1]

    # iterate over
    while task_tree:
        print("Answer 1:", "".join(steps_reversed[::-1]))
        # remove steps that have been processed
        for parent, children in task_tree.items():
            for step in steps_to_process:
                children.discard(step)

        steps_to_process = [parent for parent, children in task_tree.items() if not children]
        steps_reversed += sorted(steps_to_process)[::-1]
        # update task tree
        task_tree = {parent: children for parent, children in task_tree.items() if children}
        # print("task_tree", task_tree)
        # print("steps_to_process", steps_to_process)
        # print("steps_reversed", steps_reversed)

    print("Answer 1:", "".join(steps_reversed[::-1]))
    print("JOYAKBENSQRVXGIUWTZFMDHLPC" == "".join(steps_reversed[::-1]))
