#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

test_input="""7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_02"]

real_input = list(fileinput.input())

def is_safe(levels):
    diffs = list(map(lambda p: p[1] - p[0], itertools.pairwise(levels)))
    safe = all(map(lambda e : e > 0, diffs)) or all(map(lambda e : e < 0, diffs))
    safe = safe and all(map(lambda e : abs(e) >= 1 and abs(e) <= 3, diffs))
    return safe

def work_p1(inputs):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        levels = list(map(int, line.split()))
        if is_safe(levels):
            ret += 1
    return ret

def work_p2(inputs):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        levels = list(map(int, line.split()))
        if is_safe(levels):
            ret += 1
        else:
            for i in range(len(levels)):
                levels_ = levels[0:i] + levels[i+1:]
                if is_safe(levels_):
                    ret += 1
                    break
    return ret

def test_p1():
    assert(work_p1(test_input) == 2)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 4)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
