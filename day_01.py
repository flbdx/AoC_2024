#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""3   4
4   3
2   5
1   3
3   9
3   3
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_01"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    ll, lr = [], []
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        l, r = map(int, line.split())
        ll.append(l)
        lr.append(r)
    return ll, lr

def work_p1(inputs):
    ll, lr = read_inputs(inputs)
    
    s = 0
    for l, r in zip(sorted(ll), sorted(lr)):
        s += abs(l - r)
    return s


def work_p2(inputs):
    from collections import Counter
    ll, lr = read_inputs(inputs)
    
    cr = Counter(lr)
    
    s = 0
    for n in ll:
        s += n * cr.get(n, 0)
    return s

def test_p1():
    assert(work_p1(test_input) == 11)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 31)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
