#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_20"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    walls = set()
    start = None
    end = None

    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, c in enumerate(line):
            p = x + 1j*y
            if c == '#':
                walls.add(p)
            elif c == 'S':
                start = p
            elif c == 'E':
                end = p
    
    return walls, start, end

def work_p1(inputs, threshold=100):
    walls, start, end = read_inputs(inputs)

    distances = {}

    p = end
    s = 0
    distances[p] = 0
    path = [end]
    while p != start:
        for d in (1, -1, 1j, -1j):
            np = p + d
            if np in distances:
                continue
            if np in walls:
                continue
            s += 1
            distances[np] = s
            path.append(np)
            p = np
            break
    
    path_s = set(path)
    path = list(reversed(path))

    cheats_by_gain = {}
    
    for p in path:
        for d in (1, -1, 1j, -1j):
            np1 = p + d
            np2 = p + d + d
            if np1 in walls and np2 in path_s:
                delta = distances[p] - distances[np2] - 2
                if delta > 0:
                    cheats_by_gain[delta] = cheats_by_gain.get(delta, 0) + 1
    
    ret = 0
    for k, g in cheats_by_gain.items():
        if k >= threshold:
            ret += g
    
    return ret



def work_p2(inputs, threshold=100):
    walls, start, end = read_inputs(inputs)

    distances = {}

    p = end
    s = 0
    distances[p] = 0
    path = [end]
    while p != start:
        for d in (1, -1, 1j, -1j):
            np = p + d
            if np in distances:
                continue
            if np in walls:
                continue
            s += 1
            distances[np] = s
            path.append(np)
            p = np
            break
    
    path_s = set(path)
    path = list(reversed(path))

    cheats_by_gain = {}

    for p in path:
        for cheat_len in range(2, 21):
            for x in range(-cheat_len, cheat_len+1):
                tmp = cheat_len - abs(x)
                for y in set([- tmp, tmp]):
                    np = p + x + y*1j
                    if np in path_s:
                        delta = distances[p] - distances[np] - cheat_len
                        if delta > 0:
                            cheats_by_gain[delta] = cheats_by_gain.get(delta, 0) + 1
    
    ret = 0
    for k, g in cheats_by_gain.items():
        if k >= threshold:
            ret += g
    
    return ret

def test_p1():
    assert(work_p1(test_input, threshold=12) == 8)
test_p1()

def p1():
    print(work_p1(real_input, threshold=100))
p1()

def test_p2():
    assert(work_p2(test_input, threshold=50) == 285)
test_p2()

def p2():
    print(work_p2(real_input, threshold=100))
p2()
