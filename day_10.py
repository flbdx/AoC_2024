#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input="""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_10"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    max_x, max_y = 0, 0
    grid = {}

    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            grid[(x,y)] = int(c)
            max_x = max(max_x, x)
        max_y = max(max_y, y)
    
    return grid, max_x+1, max_y+1

def work_p1(inputs):
    grid, width, height = read_inputs(inputs)

    trailheads = {}

    for pos, value in grid.items():
        if value != 0:
            continue

        queue = deque()
        trail = (pos,)
        queue.append((trail, value))

        while len(queue):
            trail, value = queue.pop()
            if value == 9:
                trailheads.setdefault(trail[0], set()).add(trail[-1])
            coord = trail[-1]
            for d in ((1,0), (0,-1), (-1,0), (0,1)):
                npos = (coord[0] + d[0], coord[1] + d[1])
                if grid.get(npos, None) == value + 1:
                    ntrail = trail + (npos,)
                    queue.append((ntrail, value+1))
        
    return sum(len(v) for _, v in trailheads.items())

def work_p2(inputs):
    grid, width, height = read_inputs(inputs)

    trailheads = {}

    for pos, value in grid.items():
        if value != 0:
            continue

        queue = deque()
        trail = (pos,)
        queue.append((trail, value))

        while len(queue):
            trail, value = queue.pop()
            if value == 9:
                trailheads[trail[0]] = trailheads.get(trail[0], 0) + 1
            coord = trail[-1]
            for d in ((1,0), (0,-1), (-1,0), (0,1)):
                npos = (coord[0] + d[0], coord[1] + d[1])
                if grid.get(npos, None) == value + 1:
                    ntrail = trail + (npos,)
                    queue.append((ntrail, value+1))

    return sum(v for _, v in trailheads.items())

def test_p1():
    assert(work_p1(test_input) == 36)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 81)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
