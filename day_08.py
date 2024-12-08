#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import itertools

test_input="""............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_08"]

real_input = list(fileinput.input())

def read_grid(inputs):
    max_x = 0
    max_y = 0

    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            continue
        max_y = max(max_y, y)
        for x, c in enumerate(line):
            if c != '.':
                grid.setdefault(c, []).append((x, y))
            max_x = max(max_x, x)
    
    return grid, max_x + 1, max_y + 1

def work_p1(inputs):
    grid, width, height = read_grid(inputs)

    antinodes = set()

    def in_grid(p):
        return p[0] >= 0 and p[0] < width and p[1] >= 0 and p[1] < height

    for freq, coords in grid.items():
        for p1, p2 in itertools.combinations(coords, 2):
            v = (p2[0] - p1[0], p2[1] - p1[1])
            a1 = (p2[0] + v[0], p2[1] + v[1])
            a2 = (p1[0] - v[0], p1[1] - v[1])
            
            if in_grid(a1):
                antinodes.add(a1)
            if in_grid(a2):
                antinodes.add(a2)

    return len(antinodes)

def work_p2(inputs):
    grid, width, height = read_grid(inputs)

    antinodes = set()

    def in_grid(p):
        return p[0] >= 0 and p[0] < width and p[1] >= 0 and p[1] < height

    for freq, coords in grid.items():
        for p1, p2 in itertools.combinations(coords, 2):
            v = (p2[0] - p1[0], p2[1] - p1[1])
            antinodes.add(p1)
            p = (p1[0] + v[0], p1[1] + v[1])
            while in_grid(p):
                antinodes.add(p)
                p = (p[0] + v[0], p[1] + v[1])
            p = (p1[0] - v[0], p1[1] - v[1])
            while in_grid(p):
                antinodes.add(p)
                p = (p[0] - v[0], p[1] - v[1])

    return len(antinodes)

def test_p1():
    assert(work_p1(test_input) == 14)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 34)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
