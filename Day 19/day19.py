#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day19.py
"""
Advent of Code Day 19
https://adventofcode.com/2018/day/19

Copyright David Hoffman, 2018
"""

import re
import numpy as np
import tqdm
re_digits = re.compile(r"\d+")

# int = np.uint64

np.seterr(over="raise")

def strip_digits(input_):
    """Strip numbers from a string"""
    return list(map(int, re_digits.findall(input_)))

# Addition:


def addr(register, A, B, C):
    """(add register) stores into register C the result of adding register A and register B."""
    register[C] = register[A] + register[B]
    return register


def addi(register, A, B, C):
    """(add immediate) stores into register C the result of adding register A and value B."""
    register[C] = register[A] + B
    return register

# Multiplication:


def mulr(register, A, B, C):
    """(multiply register) stores into register C the result of multiplying register A and register B."""
    register[C] = register[A] * register[B]
    return register


def muli(register, A, B, C):
    """(multiply immediate) stores into register C the result of multiplying register A and value B."""
    register[C] = register[A] * B
    return register

# Bitwise AND:


def banr(register, A, B, C):
    """(bitwise AND register) stores into register C the result of the bitwise AND of register A and register B."""
    register[C] = register[A] & register[B]
    return register


def bani(register, A, B, C):
    """(bitwise AND immediate) stores into register C the result of the bitwise AND of register A and value B."""
    register[C] = register[A] & B
    return register

# Bitwise OR:


def borr(register, A, B, C):
    """(bitwise OR register) stores into register C the result of the bitwise OR of register A and register B."""
    register[C] = register[A] | register[B]
    return register


def bori(register, A, B, C):
    """(bitwise OR immediate) stores into register C the result of the bitwise OR of register A and value B."""
    register[C] = register[A] | B
    return register

# Assignment:


def setr(register, A, B, C):
    """(set register) copies the contents of register A into register C. (Input B is ignored.)"""
    register[C] = register[A]
    return register


def seti(register, A, B, C):
    """(set immediate) stores value A into register C. (Input B is ignored.)"""
    register[C] = A
    return register

# Greater-than testing:


def gtir(register, A, B, C):
    """(greater-than immediate/register) sets register C to 1 if value A is greater than register B. Otherwise, register C is set to 0."""
    register[C] = int(A > register[B])
    return register


def gtri(register, A, B, C):
    """(greater-than register/immediate) sets register C to 1 if register A is greater than value B. Otherwise, register C is set to 0."""
    register[C] = int(register[A] > B)
    return register


def gtrr(register, A, B, C):
    """(greater-than register/register) sets register C to 1 if register A is greater than register B. Otherwise, register C is set to 0."""
    register[C] = int(register[A] > register[B])
    return register

# Equality testing:


def eqir(register, A, B, C):
    """(equal immediate/register) sets register C to 1 if value A is equal to register B. Otherwise, register C is set to 0."""
    register[C] = int(A == register[B])
    return register


def eqri(register, A, B, C):
    """(equal register/immediate) sets register C to 1 if register A is equal to value B. Otherwise, register C is set to 0."""
    register[C] = int(register[A] == B)
    return register


def eqrr(register, A, B, C):
    """(equal register/register) sets register C to 1 if register A is equal to register B. Otherwise, register C is set to 0."""
    register[C] = int(register[A] == register[B])
    return register

ALL_OPS = dict(
    addr=addr,
    addi=addi,
    mulr=mulr,
    muli=muli,
    banr=banr,
    bani=bani,
    borr=borr,
    bori=bori,
    setr=setr,
    seti=seti,
    gtir=gtir,
    gtri=gtri,
    gtrr=gtrr,
    eqir=eqir,
    eqri=eqri,
    eqrr=eqrr
)

assert len(ALL_OPS) == 16

test_input = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""


def parse(input_):
    """"""
    lines = input_.splitlines()
    ip = strip_digits(lines[0])[0]
    instructions = []
    for line in lines[1:]:
        instructions.append([line.split()[0]] + strip_digits(line))

    return ip, instructions

if __name__ == '__main__':
    ip, instructions = parse(test_input)

    with open("input.txt", "r") as fp:
        ip, instructions = parse(fp.read())

    print(ip, instructions)
    print(len(instructions))
    
    init_register = new_register = [int(0)] * 6
    # while ip < len(instructions):
    for i in tqdm.trange(10_000_000):
        instruction = instructions[ip]
        old_register = new_register[:]
        # new_register[1] = 0
        # print(new_register)
        new_register = ALL_OPS[instruction[0]](new_register, *instruction[1:])
        # print("ip={} {} {} {}".format(ip, old_register, instruction, new_register))
        new_register[0] = new_register[0] + 1
        ip = new_register[0]


    print("ip={} {} {} {}".format(ip, old_register, instruction, new_register))
