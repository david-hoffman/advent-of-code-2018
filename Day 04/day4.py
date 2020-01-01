#!/usr/bin/env python
# -*- coding: utf-8 -*-
# day4.py
"""
Advent of Code Day 4
https://adventofcode.com/2018/day/4

Copyright David Hoffman, 2018
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime


def parse_line(line):
    """Parse a line from input into date and string"""
    date, string = [a.replace("[", "") for a in line.split("]")]
    date = datetime.strptime(date, "%Y-%m-%d %H:%M")
    return date, string


def data():
    """A generator yielding parsed data as slices"""
    with open("input.txt", "r") as file:
        for line in file:
            yield parse_line(line)


def convert_minutes(minutes):
    awake = np.ones(60, dtype=bool)
    for i, minute in enumerate(minutes):
        awake[minute:] = i % 2
    return awake


if __name__ == "__main__":
    df = pd.DataFrame([d for d in data()], columns=("date", "string")).sort_values("date")
    list_of_guards = []
    minutes = None
    for i, date, string in df.itertuples():
        if "Guard" in string:
            if minutes is not None:
                list_of_guards.append((guard_num, minutes))

            guard_num = int(re.findall(r"\d+", string)[0])
            minutes = []
        else:
            minutes.append(date.minute)

    # minutes asleep are the opposite of minutes awake
    df2 = pd.DataFrame(
        [
            (l[0], l[1], convert_minutes(l[1]), (~convert_minutes(l[1])).sum())
            for l in list_of_guards
        ],
        columns=("guard_num", "points", "awake", "sleep_time"),
    )

    total_sleep = df2.groupby("guard_num").sleep_time.sum()
    sleepiest_guard_num = total_sleep.idxmax()
    sleepiest_guard = df2[df2.guard_num == sleepiest_guard_num]

    sleepiest_minute = np.array([~d for d in sleepiest_guard.awake]).sum(0).argmax()

    print("Answer 1:", sleepiest_minute * sleepiest_guard_num)

    minute_of_most_sleep = df2.groupby("guard_num").awake.agg(
        lambda x: (~np.stack(x)).sum(0).argmax()
    )
    minutes_of_sleep = df2.groupby("guard_num").awake.agg(lambda x: (~np.stack(x)).sum(0).max())

    guard_num = minutes_of_sleep.idxmax()
    minute = minute_of_most_sleep[guard_num]
    print("Answer 2:", guard_num * minute)
