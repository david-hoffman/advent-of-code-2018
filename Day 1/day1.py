#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day1.py
"""
Advent of Code Day 1
https://adventofcode.com/2018/day/1

Copyright David Hoffman, 2018
"""

import pandas as pd
import numpy as np
import itertools as itt


# Part 1

# read in data
freqs = pd.read_csv("input.txt", header=None)[0].values

# Part 2
# set up a set of all frequencies we've seen
seen_berfore = set()
# and an accumulator
accum = 0

# cycle endlessly through frequencies
for i in itt.cycle(freqs):
    # updating the accumulator
    accum += i
    # checking if it's been seen
    if accum in seen_berfore:
        break
    # updating the set
    seen_berfore.add(accum)

if __name__ == "__main__":
    print("Answer 1:", freqs.sum())
    print("Answer 2:", accum)
