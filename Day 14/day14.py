#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day14.py
"""
Advent of Code Day 14
https://adventofcode.com/2018/day/14

Copyright David Hoffman, 2018
"""

from collections import deque
import tqdm


def run_simulation(n):
    elf0 = 3
    elf1 = 7
    elf0_idx = 0
    elf1_idx = 1
    d = deque((elf0, elf1))
    for i in tqdm.trange(n + 10):
        new_score = elf0 + elf1
        d.extend(map(int, str(new_score)))
        # rotate
        elf0_idx = (elf0 + 1 + elf0_idx) % len(d)
        elf0 = d[elf0_idx]

        elf1_idx = (elf1 + 1 + elf1_idx) % len(d)
        elf1 = d[elf1_idx]
    return "".join(str(d[i]) for i in range(n, n + 10))

if __name__ == '__main__':

    tests = (
        (9, "5158916779"),
        (5, "0124515891"),
        (18, "9251071085"),
        (2018, "5941429882")
    )
    for input_, result in tests:
        assert run_simulation(input_) == result

    print("Answer 1:", run_simulation(637061))
