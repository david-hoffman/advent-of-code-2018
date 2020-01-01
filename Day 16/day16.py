#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day16.py
"""
Advent of Code Day 16
https://adventofcode.com/2018/day/16

Copyright David Hoffman, 2018
"""

import re

re_digits = re.compile(r"\d+")


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


ALL_OPS = set(
    (
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr,
    )
)

assert len(ALL_OPS) == 16


def test_op(op, input_register, instruction, output_register):
    opcode, A, B, C = instruction
    test_output = op(list(input_register), A, B, C)
    return tuple(test_output) == tuple(output_register)


def possible_ops(input_register, instruction, output_register):
    return {op for op in ALL_OPS if test_op(op, input_register, instruction, output_register)}


if __name__ == "__main__":

    with open("input.txt", "r") as fp:
        input_ = fp.read()

    samples = []
    # samples are split by two returns
    for bunch in input_.split("\n\n"):
        try:
            before, instruction, after = bunch.splitlines()
        except ValueError:
            continue
        samples.append((strip_digits(before), strip_digits(instruction), strip_digits(after)))

    # we know that the last bunch is the program
    program = list(map(strip_digits, bunch.splitlines()))

    # calculate the number of possible ops for each sample
    counts = [len(possible_ops(*sample)) for sample in samples]
    # sum all with 3 or more
    print("Answer 1:", sum(count > 2 for count in counts))

    # make a dictionary of op codes with a set
    OP_CODES = dict.fromkeys(range(len(ALL_OPS)), ALL_OPS)

    # for each sample update the possible operations
    for sample in samples:
        op_code = sample[1][0]
        OP_CODES[op_code] = OP_CODES[op_code] & possible_ops(*sample)

    # hopefully there will be at least one op code with only one operation after the above
    # then we can iterate through removing the singular ops from the other sets until
    # we only have one op per op code
    while max(map(len, OP_CODES.values())) > 1:
        for op_code in OP_CODES:
            if len(OP_CODES[op_code]) == 1:
                single = OP_CODES[op_code]
                for op_code2 in OP_CODES:
                    if op_code2 == op_code:
                        continue
                    OP_CODES[op_code2] = OP_CODES[op_code2] - single

    # make sure that we've seen all the operations
    test_set = set()
    for op_code in OP_CODES.values():
        test_set = test_set | op_code

    assert len(ALL_OPS) == len(test_set)

    # convert the dictionary into a mapping of cuntions
    OP_CODES = {k: v.pop() for k, v in OP_CODES.items()}

    def execute(command, register):
        """Execute the command on a register"""
        op, A, B, C = command
        return OP_CODES[op](register, A, B, C)

    # start with empty register
    register = [0, 0, 0, 0]

    # iterate through program
    for command in program:
        execute(command, register)

    print("Answer 2:", register[0])
