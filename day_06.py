#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_06"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    grid = set()
    pos = None
    max_x, max_y = 0, 0
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        max_y = max(y, max_y)
        for x, c in enumerate(line):
            if c == '#':
                grid.add(x + 1j*y)
            elif c == '^':
                pos = x + 1j*y
            max_x = max(x, max_x)
    
    return (grid, pos, max_x+1, max_y+1)

def work_p1(inputs):
    grid, guard, width, height = read_inputs(inputs)
    direction = -1j
    turn_right = lambda d : d * 1j
    visited = set()
    visited.add(guard)

    while True:
        next_p = guard + direction
        if next_p in grid:
            direction = turn_right(direction)
            continue
        else:
            if next_p.real < 0 or next_p.real >= width:
                break
            if next_p.imag < 0 or next_p.imag >= height:
                break
            guard = next_p
            visited.add(guard)
    
    return len(visited)



def work_p2(inputs):
    grid, guard, width, height = read_inputs(inputs)
    direction = -1j
    turn_right = lambda d : d * 1j
    visited = set()
    pos = guard
    visited.add(pos)

    while True:
        next_p = pos + direction
        if next_p in grid:
            direction = turn_right(direction)
            continue
        else:
            if next_p.real < 0 or next_p.real >= width:
                break
            if next_p.imag < 0 or next_p.imag >= height:
                break
            pos = next_p
            visited.add(pos)
    
    res = 0
    obstacle_candidates = set(visited)
    obstacle_candidates.remove(guard)
    for obstacle in obstacle_candidates:
        grid.add(obstacle)
        visited = set()
        pos = guard
        direction = -1j

        while True:
            next_p = pos + direction
            if next_p in grid:
                direction = turn_right(direction)
                continue
            elif (next_p, direction) in visited:
                res += 1
                break
            else:
                if next_p.real < 0 or next_p.real >= width:
                    break
                if next_p.imag < 0 or next_p.imag >= height:
                    break
                pos = next_p
                visited.add((pos, direction))
        
        grid.remove(obstacle)
    
    return res

def test_p1():
    assert(work_p1(test_input) == 41)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 6)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
