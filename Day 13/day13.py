#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day13.py
"""
Advent of Code Day 13
https://adventofcode.com/2018/day/13

Copyright David Hoffman, 2018
"""

import numpy as np
from itertools import cycle


# dictionary of headings, up and down are reversed
# due to array ordering (indices increase going down a column)
Heading = dict(UP=(-1, 0), DOWN=(1, 0), LEFT=(0, -1), RIGHT=(0, 1))

# Reversed heading for testing purposes
HeadingReversed = {v: k for k, v in Heading.items()}

# mapping for initial cart positions
InitCartPositions = {">": ("RIGHT", "-"), "<": ("LEFT", "-"), "^": ("UP", "|"), "v": ("DOWN", "|")}

# reverse mapping for making ASCII output
InitCartPositionsReversed = {
    Heading[heading]: char for char, (heading, replacement) in InitCartPositions.items()
}

# Turn matrices, note that they're flipped too
Turns = {
    # flip
    "/": np.array([[0, -1], [-1, 0]]),
    # flip and negate
    "\\": np.array([[0, 1], [1, 0]]),
    "straight": np.eye(2, dtype=int),
    "-": np.eye(2, dtype=int),
    "|": np.eye(2, dtype=int),
    "right": np.array([[0, 1], [-1, 0]]),
    "left": np.array([[0, -1], [1, 0]]),
}


class Cart(object):
    """Object representing elves carts"""

    def __init__(self, position, heading, map_):
        """Initialize cart with position, heading and map it's on"""
        self.position = position
        self.heading = heading
        self.map = map_
        self.cycle = cycle(("left", "straight", "right"))
        self.crashed = False

    @property
    def intersection(self):
        """Get the next turn at an intersection"""
        return next(self.cycle)

    def update(self):
        """update position of cart"""
        if self.crashed:
            # if crashed don't do anything
            return None

        # where are we on the map
        map_piece = self.map[self.position[0], self.position[1]]

        # get next intersection move if we have it
        if map_piece == "+":
            map_piece = self.intersection
        # should we be turning?
        turn = Turns[map_piece]
        # apply turn
        self.heading = turn @ self.heading
        # update position
        self.position = self.position + self.heading

    def __str__(self):
        """Debug printout"""
        return "Cart #{} @ {} heading {}".format(
            self.sortkey, self.position, HeadingReversed[tuple(self.heading)]
        )

    @property
    def sortkey(self):
        """sort key based on position"""
        y, x = self.position
        ny, nx = self.map.shape
        return y * nx + x


def parse(input_):
    """Parse input into carts and map with map characters fixed"""
    map_ = np.array([[char for char in line] for line in input_.splitlines()])
    carts = []
    for cart_type, (heading, replacement) in InitCartPositions.items():
        for pos in np.argwhere(map_ == cart_type):
            carts.append(Cart(pos, Heading[heading], map_))
            map_[pos[0], pos[1]] = replacement

    return carts, map_


def format_map(carts, map_):
    """Format map for output"""
    # make a copy so as not to mess up original
    new_map = map_.copy()
    for cart in carts:
        y, x = cart.position
        new_map[y, x] = InitCartPositionsReversed[tuple(cart.heading)]
    return "\n".join(["".join(line) for line in new_map])


test_input = r"""/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/   """

if __name__ == "__main__":

    print("Testing turning matrices:")
    for turn, mat in Turns.items():
        for heading, arr in Heading.items():
            print(
                "{: >8s}: {: ^6s} --> {: ^6s}".format(
                    turn, heading, HeadingReversed[tuple(mat @ arr)]
                )
            )

    # carts, map_ = parse(test_input)

    with open("input.txt", "r") as fp:
        carts, map_ = parse(fp.read())

    print(format_map(carts, map_))

    # play game until end
    # copy of carts list
    crashed_cars = []

    while len(carts) > 1:
        for cart in sorted(carts, key=lambda x: x.sortkey):
            cart.update()
            for other_cart in carts:
                if cart.sortkey == other_cart.sortkey and other_cart is not cart:
                    cart.crashed = other_cart.crashed = True
                    crashed_cars.append(cart)
                    crashed_cars.append(cart)
        carts = [cart for cart in carts if not cart.crashed]
        # print(format_map(carts, map_))

    print("Answer 1: {},{}".format(*crashed_cars[0].position[::-1]))
    print("Answer 2: {},{}".format(*carts[0].position[::-1]))
