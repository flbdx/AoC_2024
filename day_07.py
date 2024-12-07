#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools
import math

test_input="""190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_07"]

real_input = list(fileinput.input())

def operator_add(a, b):
    return a + b
def operator_mul(a, b):
    return a * b
def operator_concat(a, b):
    e = math.floor(math.log10(b)) + 1
    return a * (10**e) + b

def work(inputs, part2=False):
    all_operators = (operator_add, operator_mul, operator_concat) if part2 else (operator_add, operator_mul)

    def test(operands, operators, target):
        r = operands[0]
        for i, operator in enumerate(operators):
            r = operator(r, operands[i+1])
            if r > target:
                return False
        return r == target


    result = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        sep = line.index(": ")
        target, operands = line[:sep], line[sep+2:]
        target = int(target)
        operands = tuple(map(int, operands.split(" ")))

        for operators in itertools.product(all_operators, repeat=len(operands) - 1):
            if test(operands, operators, target):
                result += target
                break

    return result

def test_p1():
    assert(work(test_input) == 3749)
test_p1()

def p1():
    print(work(real_input))
p1()

def test_p2():
    assert(work(test_input, part2=True) == 11387)
test_p2()

def p2():
    print(work(real_input, part2=True))
p2()
