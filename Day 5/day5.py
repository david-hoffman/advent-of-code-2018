#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day5.py
"""
Advent of Code Day 5
https://adventofcode.com/2018/day/1

Copyright David Hoffman, 2018
"""

import string


def react(string):
    """React polymer, 1 time"""
    old, new, remaining = string[0], string[1], string[2:]
    reacted = ""
    while len(remaining):
        # compare
        if old.lower() == new.lower() and old != new:
            # they react!
            try:
                old, new, remaining = remaining[0], remaining[1], remaining[2:]
            except IndexError:
                # this takes care of odd numbers
                return reacted + remaining

        else:
            # they don't react
            reacted += old
            old = new
            new = remaining[0]
            remaining = remaining[1:]

    # react final pair if necessary
    if old.lower() == new.lower() and old != new:
        return reacted
    return reacted + old + new


def react_all(string):
    """React to completion"""
    reacted = react(string)
    while reacted != string:
        # keep on reacting until no changes
        string = reacted
        reacted = react(string)
    return reacted


def data():
    """get long string"""
    with open("input.txt", "r") as fp:
        return fp.read().strip("\n")


if __name__ == '__main__':
    input_ = data()
    reacted = react_all(input_)
    print("Answer 1:", len(reacted))

    results = []
    for letter in string.ascii_lowercase:
        new_input = input_.replace(letter, "").replace(letter.upper(), "")
        # print(len(new_input))
        results.append(len(react_all(new_input)))

    print("Answer 2:", min(results))
