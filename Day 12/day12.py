#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day12.py
"""
Advent of Code Day 12
https://adventofcode.com/2018/day/12

Copyright David Hoffman, 2018
"""

import numpy as np
import matplotlib.pyplot as plt
import tqdm

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
    return np.array(list(map(int, result))).astype(bool)


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


def expand(current_state, idx, rule_size):
    """Expand state and idx if necessary"""
    plant_positions = np.argwhere(current_state)
    pad_left = rule_size - plant_positions.min()
    pad_right = plant_positions.max() - len(current_state) + rule_size
    
    pad_left = max(pad_left, 0)
    pad_right = max(pad_right, 0)

    if pad_left == 0 and pad_right == 0:
        return current_state, idx

    # update state
    new_state = np.pad(current_state, ((pad_left, pad_right),), "constant")

    # update idx
    new_idx = np.arange(len(new_state)) + idx.min() - pad_left

    return new_state, new_idx


def grow_plants2(input_, generations, generator=False):
    split = input_.strip("\n").split("\n")
    # parse input
    old_state = parse_pattern(split[0].split()[-1])
    idx = np.arange(len(old_state))

    # get rules
    rules = get_rules(split[2:])

    # we need to pad the init state by the number of generations + the length of rules on both sides!
    rule_size = rules.shape[-1]

    for gen in range(generations):
        old_state, idx = expand(old_state, idx, rule_size)
        new_state = np.zeros_like(old_state)
        for i, a in enumerate(rolling_window(old_state, rule_size)):
            new_state[i + rule_size // 2] = (a == rules).all(1).any()

        old_state = new_state
        yield old_state, idx


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

    # test dynamic algorithm
    for final_state, final_idx in grow_plants2(test_input, 20):
        pass

    assert (final_idx[final_state]).sum() == 325

    # from reddit assume that pattern must form, assume we asympototically
    # reach linear growth
    # iterate through states
    for gen, (state, idx) in enumerate(grow_plants2(input_, 50000000000)):
        # initialize
        if gen == 0:
            old_val = idx[state].sum()
            continue
        new_val = idx[state].sum()
        # initialize
        if gen == 1:
            d_old = new_val - old_val
            continue
        d_new = new_val - old_val
        # check if differnce is zero
        if d_new - d_old == 0:
            counter += 1
            # make sure difference of 0 is stabilized
            if counter > 2:
                break
        else:
            counter = 0
        d_old = d_new
        old_val = new_val

    # generation is one off from problem definition
    print("Answer 2:", (50000000000 - (gen + 1)) * d_old + new_val)
