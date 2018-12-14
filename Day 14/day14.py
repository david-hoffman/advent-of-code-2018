#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day14.py
"""
Advent of Code Day 14
https://adventofcode.com/2018/day/14

Copyright David Hoffman, 2018
"""

import tqdm


def simulator():
    elf0 = 3
    elf1 = 7
    elf0_idx = 0
    elf1_idx = 1
    scores = list((elf0, elf1))
    while True:
        new_score = elf0 + elf1
        scores.extend(map(int, str(new_score)))
        # rotate
        elf0_idx = (elf0 + 1 + elf0_idx) % len(scores)
        elf0 = scores[elf0_idx]

        elf1_idx = (elf1 + 1 + elf1_idx) % len(scores)
        elf1 = scores[elf1_idx]
        yield scores


def run_simulation(n):
    for scores in simulator():
        if len(scores) > n + 10:
            break
    return scores[n:n + 10]


def run_simulation2(pattern):
    pattern = list(map(int, pattern))
    for i, scores in enumerate(simulator()):
        test0 = scores[-len(pattern):]
        test1 = scores[-len(pattern) - 1:-1]
        if test0 == pattern or test1 == pattern:
            break

    return len(scores) - len(pattern) - (test1 == pattern)

if __name__ == '__main__':

    tests = (
        (9, "5158916779"),
        (5, "0124515891"),
        (18, "9251071085"),
        (2018, "5941429882")
    )
    for input_, result in tests:
        ans = run_simulation(input_)
        assert ans == list(map(int, result)), "{} != {}".format(ans, result)

    print("Answer 1:", "".join(map(str, run_simulation(637061))))

    tests2 = (
        ("51589", 9),
        ("01245", 5),
        ("92510", 18),
        ("59414", 2018)
    )

    for input_, result in tests2:
        ans = run_simulation2(input_)
        assert result == ans

    print("Answer 2:", run_simulation2("637061"))
