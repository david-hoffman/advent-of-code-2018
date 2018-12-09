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
    graph.add_edges_from([parse(line) for line in data])

    ans = "".join(nx.lexicographical_topological_sort(graph))
    print("Answer 1:", ans)

    task_times = []
    tasks = []
    time = 0
    while task_times or graph:
        available_tasks = [t for t in graph if t not in tasks and graph.in_degree(t) == 0]
        if available_tasks and len(task_times) < 5:
            task = min(available_tasks)  # min gets smallest task alphabetically
            task_times.append(ord(task) - 4)
            tasks.append(task)
        else:
            min_time = min(task_times)
            completed = [tasks[i] for i, v in enumerate(task_times) if v == min_time]
            task_times = [v - min_time for v in task_times if v > min_time]
            tasks = [t for t in tasks if t not in completed]
            time += min_time
            graph.remove_nodes_from(completed)

    print("Answer 2:", time)
