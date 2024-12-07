#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_04"]

real_input = list(fileinput.input())

def parse(inputs):
    m = {}
    max_x, max_y = 0, 0
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            m[x+1j*y] = c
            max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    return m, max_x + 1, max_y + 1

def work_p1(inputs):
    grid, width, height = parse(inputs)
    
    ret = 0
    for y in range(height):
        for x in range(width):
            p = x+1j*y
            for dir in ((1, -1, 1j, -1j, 1+1j, 1-1j, -1+1j, -1-1j)):
                if grid.get(p) == "X" and grid.get(p+1*dir, None) == "M" and grid.get(p+2*dir, None) == "A" and grid.get(p+3*dir, None) == "S":
                    ret += 1
    return ret

def work_p2(inputs):
    grid, width, height = parse(inputs)
    
    ret = 0
    for y in range(height):
        for x in range(width):
            p = x+1j*y

            if grid[p] == 'A':
                if grid.get(p-1-1j, None) == 'M' and grid.get(p+1+1j) == 'S' or grid.get(p-1-1j, None) == 'S' and grid.get(p+1+1j) == 'M':
                    if grid.get(p-1+1j, None) == 'M' and grid.get(p+1-1j) == 'S' or grid.get(p-1+1j, None) == 'S' and grid.get(p+1-1j) == 'M':
                        ret += 1

    return ret

def test_p1():
    assert(work_p1(test_input) == 18)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 9)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
