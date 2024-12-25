#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_25"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    locks = []
    keys = []

    it = iter(inputs)
    while True:
        try:
            lines = [next(it).strip() for _ in range(7)]
        except:
            break
        grid = {}
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                grid[(x,y)] = c
        
        grid_type = grid[(0,0)]
        heights = [0 for _ in range(5)]
        for x in range(5):
            for y in range(5):
                if grid[(x,y+1)] == grid_type:
                    heights[x] += 1
                else:
                    break
        if grid_type == '#':
            locks.append(tuple(heights))
        else:
            keys.append(tuple(5-h for h in heights))
        
        try:
            next(it)
        except:
            break

    return locks, keys

def work_p1(inputs):
    locks, keys = read_inputs(inputs)
    
    keys = list(sorted(keys))

    ret = 0
    for lock in locks:
        for key in keys:
            if key[0] + lock[0] > 5: # is that an optimisation for the last puzzle?
                break
            if all(key[i] + lock[i] <= 5 for i in range(1, 5)):
                ret += 1
    return ret

def test_p1():
    assert(work_p1(test_input) == 3)
test_p1()

def p1():
    print(work_p1(real_input))
p1()
