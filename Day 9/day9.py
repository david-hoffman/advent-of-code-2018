#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day9.py
"""
Advent of Code Day 9
https://adventofcode.com/2018/day/9

Copyright David Hoffman, 2018
"""

from itertools import cycle
import tqdm

test_input = """
9 players; last marble is worth 25 points: high score is 32
10 players; last marble is worth 1618 points: high score is 8317
13 players; last marble is worth 7999 points: high score is 146373
17 players; last marble is worth 1104 points: high score is 2764
21 players; last marble is worth 6111 points: high score is 54718
30 players; last marble is worth 5807 points: high score is 37305
"""


class circle(object):
    def __init__(self):
        self.list = [0]
        self.current_idx = 0

    def add_marble(self, marble_num):
        
        if marble_num % 23:
            if len(self.list) < 2:
                index_to_place = len(self.list)
            else:
                index_to_place = (self.current_idx + 2) % (len(self.list))
            if index_to_place is 0:
                index_to_place = len(self.list)
            self.current_idx = index_to_place
            self.list.insert(index_to_place, marble_num)
            return 0
        else:
            index_to_pop = self.current_idx - 7
            self.current_idx -= 7
            if self.current_idx < 0:
                self.current_idx = len(self.list) + self.current_idx
            popped_value = self.list.pop(index_to_pop)
            # print(marble_num, popped_value)
            return marble_num + popped_value

    def __str__(self):
        s = ""
        for i, marble in enumerate(self.list):
            if i == self.current_idx:
                s += "{: >3}".format("({})".format(marble))
            else:
                s += " {: >2} ".format(marble)
        return s


def calc_score(num_players, num_marbles):
    score = dict.fromkeys(range(num_players), 0)
    c = circle()
    # print("[-] ", c)
    for player, marble in zip(cycle(sorted(score)), tqdm.trange(1, num_marbles)):
        j = c.add_marble(marble)
        score[player] += j

    return max(score.values())


def parse(input_):
    split = input_.split()
    num_players = int(split[0])
    num_marbles = int(split[6]) + 1
    try:
        result = int(split[-1])
        return num_players, num_marbles, result
    except ValueError:
        return num_players, num_marbles


if __name__ == '__main__':
    for input_ in test_input.strip("\n").split("\n"):
        num_players, num_marbles, result = parse(input_)
        print(input_)
        assert calc_score(num_players, num_marbles) == result

    with open("input.txt", "r") as fp:
        num_players, num_marbles = parse(fp.read().strip("\n"))
    print(num_marbles)
    print("Answer 1:", calc_score(num_players, num_marbles))
    print("Answer 2:", calc_score(num_players, (num_marbles - 1) * 100 + 1))