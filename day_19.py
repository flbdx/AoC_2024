#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_19"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    towels = {}
    patterns = []

    it = iter(inputs)
    towels = {t: len(t) for t in next(it).strip().split(', ')}
    next(it)
    for line in it:
        line = line.strip()
        if len(line) == 0:
            continue
        patterns.append(line)
    
    return towels, patterns

def work_p1(inputs):
    towels, patterns = read_inputs(inputs)

    valid_patterns = set()

    def pattern_is_valid(pattern):
        if pattern in valid_patterns:
            return True
        for towel, lt in towels.items():
            if pattern == towel:
                valid_patterns.add(pattern)
                return True
            if pattern.startswith(towel):
                if pattern_is_valid(pattern[lt:]):
                    valid_patterns.add(pattern)
                    return True
        return False

    ret = 0
    for pattern in patterns:
        valid = pattern_is_valid(pattern)
        if valid:
            ret += 1
    
    return ret

def work_p2(inputs):
    towels, patterns = read_inputs(inputs)

    combinations = {}

    def count_pattern(pattern):
        cnt = combinations.get(pattern, None)
        if cnt is not None:
            return cnt

        for towel, lt in towels.items():
            if pattern == towel:
                combinations[pattern] = combinations.get(pattern, 0) + 1
            elif pattern.startswith(towel):
                cnt = count_pattern(pattern[lt:])
                combinations[pattern] = combinations.get(pattern, 0) + cnt
        
        return combinations.get(pattern, 0)
    
    ret = 0
    for pattern in patterns:
        ret += count_pattern(pattern)

    return ret

def test_p1():
    assert(work_p1(test_input) == 6)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 16)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
