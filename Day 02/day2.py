#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day2.py
"""
Advent of Code Day 2
https://adventofcode.com/2018/day/2

Copyright David Hoffman, 2018
"""

import pandas as pd
import numpy as np
import itertools as itt

# Part 1

# read in data
strings = pd.read_csv("input.txt", header=None)[0].values

# convert characters to numbers
chars = np.array([np.array(s, "c").view("uint8") for s in strings])

# calculate counts of chars
counts = [np.bincount(char) for char in chars]

# calculate counts of counts
counts_of_counts = [np.bincount(count, minlength=10) for count in counts]

# figure out which strings have characters that appear in duplicate
twos = [count[2] > 0 for count in counts_of_counts]

# figure out which strings have characters that appear in triplicate
threes = [count[3] > 0 for count in counts_of_counts]


# Part 2
# find the strings that differ by at most 1 character
for i, j in itt.combinations(chars, 2):
    if sum(i == j) == 25:
        break


if __name__ == "__main__":
    print("Answer 1:", sum(twos) * sum(threes))
    print("Answer 2:", "".join(i.view("c").astype("str")[i == j]))
