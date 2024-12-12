#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import collections

test_input_1="""AAAA
BBCD
BBCC
EEEC
""".splitlines()
test_input_2="""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
""".splitlines()
test_input_3="""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_12"]

real_input = list(fileinput.input())

class Value:
    def __init__(self, label, region=None):
        self.label = label
        self.region = region
        self.borders = {}

def read_inputs(inputs):
    max_x, max_y = 0, 0
    grid = {}
    for y, line in enumerate(inputs):
        line = line.strip()
        if len(line) == 0:
            break
        for x, l in enumerate(line):
            grid[(x,y)] = Value(l)
            max_x = max(x, max_x)
        max_y = max(y, max_y)
    
    return grid, max_x+1, max_y+1

def addp(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def create_regions(grid, width, height):
    regions = {}

    for y in range(height):
        for x in range(width):
            p = (x,y)
            v = grid.get(p)

            if v.region is not None:
                continue

            v.region = p
            regions[p] = {p}
            queue = collections.deque()
            queue.append(addp(p, (1,0)))
            queue.append(addp(p, (0,1)))

            # visited 
            while len(queue):
                np = queue.pop()
                nv = grid.get(np, None)
                if nv is None:
                    continue
                if nv.region is not None:
                    continue
                if nv.label != v.label:
                    continue
                nv.region = v.region
                regions[v.region].add(np)
                for o in ((1,0),(-1,0),(0,1),(0,-1)):
                    nnp = addp(np, o)
                    nnv = grid.get(nnp, None)
                    if nnv is not None and nnv.region is None:
                        queue.append(nnp)
    
    return regions

def work_p1(inputs):
    grid, width, height = read_inputs(inputs)

    regions = create_regions(grid, width, height)

    price = 0
    for _, region in regions.items():
        area = len(region)

        borders = 0
        for p in region:
            for o in ((1,0),(-1,0),(0,1),(0,-1)):
                np = addp(p, o)
                if np not in region:
                    borders += 1
        price += borders * area
    
    return price


def work_p2(inputs):
    grid, width, height = read_inputs(inputs)

    regions = create_regions(grid, width, height)

    # this year I will not take it easy. let's not count the corners :-)
    price = 0
    for _, region in regions.items():
        # print(sorted(list(region)))
        area = len(region)

        borders = {}
        
        for p in region:
            v = grid.get(p)

            for dir in ((1,0),(-1,0),(0,1),(0,-1)):
                border = (p, dir)
                if v.borders.get(dir, None) != None:
                    continue

                np = addp(p, dir)
                if np in region:
                    continue

                v.borders[dir] = border
                borders[border] = {border}

                queue = collections.deque()
                if dir == (1,0) or dir == (-1,0):
                    queue.append(addp(p, (0,-1)))
                    queue.append(addp(p, (0,1)))
                else:
                    queue.append(addp(p, (-1,0)))
                    queue.append(addp(p, (1,0)))
                
                visited = set()
                visited.add(p)

                while len(queue):
                    np = queue.pop()
                    visited.add(np)
                    if not np in region:
                        continue
                    nv = grid.get(np, None)
                    
                    nnp = addp(np, dir)
                    if nnp in region:
                        continue
                    nv.borders[dir] = border
                    borders[border].add((np, dir))

                    if dir == (1,0) or dir == (-1,0):
                        nnp = addp(np, (0,-1))
                        if nnp not in visited:
                            queue.append(nnp)
                        nnp = addp(np, (0,1))
                        if nnp not in visited:
                            queue.append(nnp)
                    else:
                        nnp = addp(np, (-1,0))
                        if nnp not in visited:
                            queue.append(nnp)
                        nnp = addp(np, (1,0))
                        if nnp not in visited:
                            queue.append(nnp)
                
                # print(border, borders[border])
        # print(len(borders))
        # print(borders)

        price += area * len(borders)
    
    return price

                


def test_p1():
    assert(work_p1(test_input_1) == 140)
    assert(work_p1(test_input_2) == 772)
    assert(work_p1(test_input_3) == 1930)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input_1) == 80)
    assert(work_p2(test_input_2) == 436)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
