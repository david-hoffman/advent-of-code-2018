#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day15.py
"""
Advent of Code Day 15
https://adventofcode.com/2018/day/15

Copyright David Hoffman, 2018
"""

import numpy as np
from collections import deque
import string

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

    @property
    def sortkey(self):
        """sort key based on position"""
        y, x = self.position
        ny, nx = self.map.shape
        return y * nx + x

    @property
    def alive(self):
        return self.HP > 0

    def __repr__(self):
        return "{} @ {}, ({})".format(self.__class__.__name__, self.position, self.HP)


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
            if next_char == enemy:
                # we've found the closest enemy!
                yield path + [next_pos]
            if next_char != "." or next_pos in visited:
                # we've seen this place before or we hit something
                continue
            queue.append((next_pos, path + [next_pos]))
            visited.add(next_pos)


def shortest_paths_to_enemy(unit, units):
    shortest_path = np.inf
    for path in paths_to_enemy(unit, units):
        if len(path) > shortest_path:
            break
        shortest_path = len(path)
        yield path


def place_units(units, char=True):
    """"""
    # make a copy so as not to mess up original
    new_map = units[0].map.copy()
    for i, unit in zip(string.ascii_letters, sorted(units, key=lambda x: x.sortkey)):
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
        output[y] = line + "   " + ", ".join(["{}({})".format(unit.char, unit.HP) for unit in units if unit.position[0] == y])
    return "\n".join(output)#.translate(translation_table).replace(".", "  ")


def parse(input_):
    """Parse input into units and map with map characters fixed"""
    map_ = np.array([[char for char in line] for line in input_.splitlines()])
    units = []
    for unit_type in (Goblin, Elf):
        for pos in np.argwhere(map_ == unit_type.char):
            units.append(unit_type(pos, map_))
            map_[pos[0], pos[1]] = "."
    # make map_ immutable
    map_.flags.writeable = False
    return units


def enemies_left(units):
    return len(set(unit.char for unit in units)) > 1


def run_combat(units):
    over = False
    rounds = 0
    while not over:
        for i, unit in enumerate(sorted(units, key=lambda x: x.sortkey)):
            if not unit.alive:
                continue
            if not enemies_left(units):
                over = True
                break
            # move unit
            try:
                best_path = next(shortest_paths_to_enemy(unit, units))
            except StopIteration:
                best_path = []
            if len(best_path) > 2:
                # we're not next to an enemy
                # take one step along path, note that first location is original position
                unit.position = best_path[1]
            # find targets
            possible_targets = [test_unit for test_unit in units if unit.is_neighbor(test_unit) and unit.char != test_unit.char and test_unit.alive]
            if possible_targets:
                # select target
                target = sorted(possible_targets, key=lambda x: (x.HP, x.sortkey))[0]
                # attack
                assert target.HP > 0
                target.HP -= unit.AP
        if i == len(units) - 1:
            rounds += 1

        units = [unit for unit in units if unit.alive]

    return units, rounds - 1


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

        units, rounds = run_combat(units)
        total_HP = np.sum([unit.HP for unit in units]) 
        result = total_HP * rounds
        try:
            assert result == test_result, "Result {}, total HP {}, rounds {}\n".format(result, total_HP, rounds) + format_map(units)
        except AssertionError as e:
            print(e)

    with open("input.txt", "r") as fp:
        input_ = fp.read()

    units = parse(input_)
    print(format_map(units, False))
    units, rounds = run_combat(units)
    print("+" * 80)
    print(format_map(units, False))
    print(np.sum([unit.HP for unit in units]), rounds)
