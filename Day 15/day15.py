#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day15.py
"""
Advent of Code Day 15
https://adventofcode.com/2018/day/15

Copyright David Hoffman, 2018
"""

import time
import string
import numpy as np
from collections import deque
from itertools import count

translation_table = str.maketrans("#GE", "🧱👹🧝")

# move in reading order
directions = np.array((
    (-1, 0),  # UP
    (0, -1),  # LEFT
    (0, 1),   # RIGHT
    (1, 0),   # DOWN
))


class Unit(object):
    """A base class describing a unit"""
    char = "U"
    AP = 3

    def __init__(self, position, map_):
        self.position = position
        self.map = map_
        self.HP = 200

    def is_neighbor(self, other):
        x0, y0 = self.position
        x1, y1 = other.position

        # manhattan distance is 1
        return (abs(x0 - x1) + abs(y0 - y1)) == 1

    def __bool__(self):
        return self.HP > 0

    def __repr__(self):
        return "{} @ {}, ({})".format(self.__class__.__name__, self.position, self.HP)

    def __lt__(self, other):
        return self.position < other.position


class Elf(Unit):
    """Elf class"""
    char = "E"


class Goblin(Unit):
    """Goblin class"""
    char = "G"


def paths_to_enemy(unit, units):
    """Breadth first search of paths"""
    enemy = "GE".replace(unit.char, "")
    new_map = place_units(units)
    #
    visited = set()
    queue = deque()
    queue.append((tuple(unit.position), [tuple(unit.position)]))
    while queue:
        (vertex, path) = queue.popleft()
        for next_pos in vertex + directions:
            next_pos = tuple(next_pos)
            next_char = new_map[next_pos[0], next_pos[1]]
            if next_pos in visited:
                # we've seen this place before or we hit something
                continue
            if next_char == enemy:
                # we've found the closest enemy!
                yield path[1:]
                # do not add enemies to seen list, we want all paths to them!
                continue
            visited.add(next_pos)
            if next_char != ".":
                continue
            queue.append((next_pos, path + [next_pos]))


def shortest_paths_to_enemy(unit, units):
    shortest_path = np.inf
    for path in paths_to_enemy(unit, units):
        if len(path) > shortest_path:
            break
        shortest_path = len(path)
        yield path


def place_units(units, char=True):
    """"""
    for i, unit in zip(string.ascii_letters, sorted(units)):
        if i == "a":
            # make a copy so as not to mess up original
            new_map = unit.map.copy()
        y, x = unit.position
        if char:
            new_map[y, x] = unit.char
        else:
            new_map[y, x] = i

    return new_map


def format_map(units, char=True):
    """Format map for output"""
    output = place_units(units, char)
    output = ["".join(line) for line in output]
    for y, line in enumerate(output):
        output[y] = line + "   " + ", ".join(["{}({})".format(unit.char, unit.HP) for unit in sorted(units) if unit.position[0] == y])
    return "\n".join(output)


def parse(input_):
    """Parse input into units and map with map characters fixed"""
    map_ = np.array([[char for char in line] for line in input_.splitlines()])
    units = []
    for unit_type in (Goblin, Elf):
        for pos in np.argwhere(map_ == unit_type.char):
            units.append(unit_type(tuple(pos), map_))
            map_[pos[0], pos[1]] = "."
    # make map_ immutable
    map_.flags.writeable = False
    return units


def enemies_left(units):
    return len(set(unit.char for unit in units)) > 1


def run_combat(units):
    over = False
    rounds = 0
    maps = []
    while enemies_left(units):
        units.sort()
        for i, unit in enumerate(units):
            if not enemies_left(filter(None, units)):
                # any enemies left?
                break
            if not unit:
                # if the unit was killed during a round ignore it for now
                continue
            # move unit
            # find all shortest paths, make sure to clear dead units from search!
            best_paths = list(shortest_paths_to_enemy(unit, filter(None, units)))
            # we're already sorted by first step and length so only need to sort by target position reading order
            if len(best_paths) and min(len(path) for path in best_paths):
                # found at least one possible step
                # test = best_paths[:]
                best_paths.sort(key=lambda x: x[-1])
                # assert test == best_paths
                best_path = best_paths[0]
                # move to new spot, make sure it's a neighbor
                assert np.abs(np.subtract(unit.position, best_path[0])).sum() == 1, "{} ---> {}".format(unit.position, best_path[0])
                unit.position = best_path[0]
                
            # find targets
            possible_targets = sorted([test_unit for test_unit in units if unit.is_neighbor(test_unit) and unit.char != test_unit.char and test_unit])
            if possible_targets:
                # select target
                target = sorted(possible_targets, key=lambda x: (x.HP, x.position[0], x.position[1]))[0]
                # attack
                assert target
                assert unit
                assert not (target is unit)
                target.HP -= unit.AP

        else:
            # round completed without break?
            rounds += 1
            maps.append(format_map(filter(None, units)))

        units = list(filter(None, units))
    maps.append(format_map(filter(None, units)))
    return units, np.sum([unit.HP for unit in filter(None, units)]), rounds, maps


def clean_test_input(test_input):
    num = len(test_input.split()[0])
    return "\n".join([i[:num] for i in test_input.strip().splitlines()])

test_inputs = []
test_results = []

test_inputs.append("""
#######   
#.G...#   G(200)
#...EG#   E(200), G(200)
#.#.#G#   G(200)
#..G#E#   G(200), E(200)
#.....#   
#######
""")

test_results.append(27730)

test_inputs.append("""
#######       #######
#G..#E#       #...#E#   E(200)
#E#E.E#       #E#...#   E(197)
#G.##.#  -->  #.E##.#   E(185)
#...#E#       #E..#E#   E(200), E(200)
#...E.#       #.....#
#######       #######
""")

test_results.append(36334)

test_inputs.append("""
#######       #######   
#E..EG#       #.E.E.#   E(164), E(197)
#.#G.E#       #.#E..#   E(200)
#E.##E#  -->  #E.##.#   E(98)
#G..#.#       #.E.#.#   E(200)
#..E#.#       #...#.#   
#######       #######   
""")

test_results.append(39514)

test_inputs.append("""
#######       #######   
#E.G#.#       #G.G#.#   G(200), G(98)
#.#G..#       #.#G..#   G(200)
#G.#.G#  -->  #..#..#   
#G..#.#       #...#G#   G(95)
#...E.#       #...G.#   G(200)
#######       #######   
""")

test_results.append(27755)

test_inputs.append("""
#######       #######   
#.E...#       #.....#   
#.#..G#       #.#G..#   G(200)
#.###.#  -->  #.###.#   
#E#G#G#       #.#.#.#   
#...#G#       #G.G#G#   G(98), G(38), G(200)
#######       #######   
""")

test_results.append(28944)

test_inputs.append("""
#########       #########   
#G......#       #.G.....#   G(137)
#.E.#...#       #G.G#...#   G(200), G(200)
#..##..G#       #.G##...#   G(200)
#...##..#  -->  #...##..#   
#...#...#       #.G.#...#   G(200)
#.G...G.#       #.......#   
#.....G.#       #.......#   
#########       #########  
""")

test_results.append(18740)

if __name__ == '__main__':
    for test_input, test_result in zip(test_inputs, test_results):
        input_ = clean_test_input(test_input)

        units = parse(input_)

        units, total_HP, rounds, maps = run_combat(units)
        result = total_HP * (rounds - 0)
        try:
            assert result == test_result, "Result {} != {}, total HP {}, rounds {}\n".format(result, test_result, total_HP, rounds) + maps[-1] #+ "\n\n".join(["Round {}\n{}".format(i+1, map_) for i, map_ in enumerate(maps)])
        except AssertionError as e:
            print(e)

    with open("input.txt", "r") as fp:
        input_ = fp.read()

    units = parse(input_)
    units, total_HP, rounds, battle0 = run_combat(units)
    print("Answer 1:", total_HP * rounds)

    for AP in count(4):
        Elf.AP = AP
        units = parse(input_)
        starting_elves = len([unit for unit in units if unit.char == "E"])
        units, total_HP, rounds, battle1 = run_combat(units)

        remaining_elves = len([unit for unit in units if unit.char == "E"])
        if remaining_elves == starting_elves:
            break
    print("Answer 2:", total_HP * rounds)

    for battle in (battle0, battle1):
        for i, map_ in enumerate(battle):
            time.sleep(1 / 24)
            print("{:-^32s}".format("Round {}".format(i)))
            print(map_.translate(translation_table).replace(".", "  "))
        time.sleep(3)
