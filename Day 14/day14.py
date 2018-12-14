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
    for i, scores in zip(tqdm.trange(n + 10), simulator()):
        pass
    return "".join(str(scores[i]) for i in range(n, n + 10))


def run_simulation2(pattern):
    for i, scores in enumerate(tqdm.tqdm(simulator())):
        test = "".join(str(scores[i]) for i in range(len(scores) - len(pattern), len(scores)))
        if test == pattern:
            break
            
    return len(scores) - len(pattern)

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

    tests2 = (
        ("51589", 9),
        ("01245", 5),
        ("92510", 18),
        ("59414", 2018)
    )

    for input_, result in tests2:
        ans = run_simulation2(input_)
        print(input_, result, ans)
        assert result == ans

    print("Answer 2:", run_simulation2("637061"))
