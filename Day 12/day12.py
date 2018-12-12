#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day12.py
"""
Advent of Code Day 12
https://adventofcode.com/2018/day/12

Copyright David Hoffman, 2018
"""

import numpy as np

test_input = """initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #"""

test_result = """0: ...#..#.#..##......###...###...........
 1: ...#...#....#.....#..#..#..#...........
 2: ...##..##...##....#..#..#..##..........
 3: ..#.#...#..#.#....#..#..#...#..........
 4: ...#.#..#...#.#...#..#..##..##.........
 5: ....#...##...#.#..#..#...#...#.........
 6: ....##.#.#....#...#..##..##..##........
 7: ...#..###.#...##..#...#...#...#........
 8: ...#....##.#.#.#..##..##..##..##.......
 9: ...##..#..#####....#...#...#...#.......
10: ..#.#..#...#.##....##..##..##..##......
11: ...#...##...#.#...#.#...#...#...#......
12: ...##.#.#....#.#...#.#..##..##..##.....
13: ..#..###.#....#.#...#....#...#...#.....
14: ..#....##.#....#.#..##...##..##..##....
15: ..##..#..#.#....#....#..#.#...#...#....
16: .#.#..#...#.#...##...#...#.#..##..##...
17: ..#...##...#.#.#.#...##...#....#...#...
18: ..##.#.#....#####.#.#.#...##...##..##..
19: .#..###.#..#.#.#######.#.#.#..#.#...#..
20: .#....##....#####...#######....#.#..##."""

test_result = "\n".join([t.strip().split()[-1] for t in test_result.split("\n")])


def parse_pattern(pattern):
    result = pattern.replace("#", "1").replace(".", "0")
    return np.array(list(map(int, result)))


def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def get_rules(list_of_rules):
    """parse rules, if rule results in next gen being zero, ignore"""
    rules = []
    for rule in list_of_rules:
        pattern, _, result = rule.split()
        if result == ".":
            continue
        rules.append(parse_pattern(pattern))
    rules = np.asarray(rules).astype(bool)
    return rules


def grow_plants(input_, generations):
    split = input_.strip("\n").split("\n")
    # parse input
    init_state = parse_pattern(split[0].split()[-1])

    rules = get_rules(split[2:])

    # we need to pad the init state by the number of generations + the length of rules on both sides!
    rule_size = rules.shape[-1]
    all_states = np.zeros((generations, len(init_state) + 2 * (generations + rule_size)), dtype=bool)
    idx = np.arange(all_states.shape[-1]) - (generations + rule_size)
    all_states[0, (-1 < idx) & (idx < len(init_state))] = init_state

    for j in range(len(all_states) - 1):
        for i, a in enumerate(rolling_window(all_states[j], rule_size)):
            all_states[j + 1, i + rule_size // 2] = (a == rules).all(1).any()

    return all_states, idx


if __name__ == '__main__':

    all_states, idx = grow_plants(test_input, 21)

    truncated_states = (all_states[:, (idx > -4) & (idx < 36)].astype(int))
    truncated_states = ("\n".join("".join(state) for state in truncated_states.astype(str)).replace("1", "#").replace("0", "."))

    assert truncated_states == test_result
    assert 325 == (idx[all_states[-1]].sum())

    with open("input.txt", "r") as fp:
        input_ = fp.read()

    all_states, idx = grow_plants(input_, 21)
    print("Answer 1:", idx[all_states[-1]].sum())