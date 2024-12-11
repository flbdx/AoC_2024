#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import math

test_input="""125 17
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_11"]

real_input = list(fileinput.input())

def work(inputs, steps):
    line = next(iter(inputs)).strip()
    l = map(int, line.split())
    
    cache = {}

    def rec_solve(n, step):
        nonlocal cache
        if step == 0:
            return 1
        
        v = cache.get((n, step), None)
        if v is not None:
            return v
        
        if n == 0:
            v = rec_solve(1, step - 1)
        else:
            nl = math.floor(math.log10(n)) + 1
            if (nl & 1) == 0:
                exp = 10**(nl//2)
                left = n // exp
                right = n - left * exp
                v = rec_solve(left, step-1) + rec_solve(right, step-1)
            else:
                v = rec_solve(n * 2024, step-1)
        
        cache[(n, step)] = v
        return v

    return sum(rec_solve(n, steps) for n in l)

def work_p1(inputs):
    return work(inputs, 25)

def work_p2(inputs):
    return work(inputs, 75)

def test_p1():
    assert(work_p1(test_input) == 55312)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

# def test_p2():
#     assert(work_p2(test_input) == None)
# test_p2()

def p2():
    print(work_p2(real_input))
p2()
