#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
import collections

test_input="""p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_14"]

real_input = list(fileinput.input())

Robot = collections.namedtuple("Robot", list("pv"))

def read_inputs(inputs):
    re_int = re.compile(r"(-?[0-9]+)")

    robots = []

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        values = list(map(int, re_int.findall(line)))
        robots.append(Robot(p=tuple(values[0:2]), v=tuple(values[2:])))
    
    return robots

def simu(robots, width, height, cycles=100):
    nrobots = []
    for robot in robots:
        np = ((robot.p[0] + robot.v[0] * cycles) % width, (robot.p[1] + robot.v[1] * cycles) % height)
        nrobot = Robot(np, robot.v)
        nrobots.append(nrobot)
    return nrobots

def work_p1(inputs, width=101, height=103):
    robots = read_inputs(inputs)
    robots = simu(robots, width, height)

    count_top_left = 0
    count_top_right = 0
    count_bottom_left = 0
    count_bottom_right = 0
    for r in robots:
        if r.p[0] < width //2 and r.p[1] < height // 2:
            count_top_left += 1
        elif r.p[0] > width //2 and r.p[1] < height // 2:
            count_top_right += 1
        elif r.p[0] < width //2 and r.p[1] > height // 2:
            count_bottom_left += 1
        elif r.p[0] > width //2 and r.p[1] > height // 2:
            count_bottom_right += 1

    return count_top_left * count_top_right * count_bottom_left * count_bottom_right

def work_p2(inputs, width=101, height=103):
    robots = read_inputs(inputs)

    # search for a position where at least N% of the robots have at least 2 neighbours and break
    secs = 0
    while True:
        secs += 1
        robots = simu(robots, width, height, cycles=1)
        map = {r.p: r for r in robots}

        with_neighbours = 0
        for r in robots:
            count = 0
            for o in ((0,1), (0,-1), (1,0), (-1,0)):
                if ((r.p[0] + o[0]), (r.p[1] + o[1])) in map:
                    count += 1
                else:
                    break
            if count >= 2:
                with_neighbours += 1
        
        if with_neighbours > len(robots) // 3:
            count = {}
            for r in robots:
                count[r.p] = count.get(r.p, 0) + 1
            
            for y in range(height):
                s = ""
                for x in range(width):
                    c = count.get((x,y), 0)
                    if c == 0:
                        s += "."
                    else:
                        s += repr(c)
                print(s)
            
            return secs

def test_p1():
    assert(work_p1(test_input, width=11, height=7) == 12)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

# def test_p2():
#     assert(work_p2(test_input) == None)
# # test_p2()

def p2():
    print(work_p2(real_input))
p2()
