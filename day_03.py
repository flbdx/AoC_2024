#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re

test_input_1="""xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
""".splitlines()
test_input_2="""xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_03"]

real_input = list(fileinput.input())

def work_p1(inputs):
    ret = 0
    regexp = re.compile(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        for m in regexp.findall(line):
            ret += int(m[0]) * int(m[1])
    return ret

def work_p2(inputs):
    ret = 0
    regexp = re.compile(r"(do\(\))|(don't\(\))|mul\(([0-9]{1,3}),([0-9]{1,3})\)")
    
    enabled = True
    
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        for m in regexp.findall(line):
            if len(m[0]):
                enabled = True
            elif len(m[1]):
                enabled = False
            elif enabled:
                ret += int(m[2]) * int(m[3])
    return ret

def test_p1():
    assert(work_p1(test_input_1) == 161)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input_2) == 48)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
