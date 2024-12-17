#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input_1="""###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
""".splitlines()

test_input_2="""#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_16"]

real_input = list(fileinput.input())

def read_inputs(inputs):
    start = None
    end = None
    walls = set()
    width = 0

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
            width = max(width, x)
    
    return walls, start, end, width+1

def work(inputs):
    walls, start, end, width = read_inputs(inputs)

    best_cache = {}
    best_cache[(start, dir)] = 0
    
    cplx_to_bit = lambda c : 1<<(int(c.real) + int(c.imag)*width)

    class State:
        def __init__(self, position, dir, s, v):
            self.p = position       # position
            self.d = dir            # direction
            self.s = s              # score
            self.v = v              # visited nodes as a bitfield, a set would be quite slow to copy/delete
        
        def rotate_right(self):
            self.d *= 1j
            self.s += 1000
            return self
        def rotate_left(self):
            self.d *= -1j
            self.s += 1000
            return self
        def try_advance(self):
            nonlocal walls, cplx_to_bit
            np = self.p + self.d
            if np in walls or (self.v & cplx_to_bit(np)):
                return None
            self.p = np
            self.s += 1
            self.v |= cplx_to_bit(self.p)
            return self
        def copy(self):
            return State(self.p, self.d, self.s, self.v)
            

    queue = deque()
    queue.append(State(start, 1, 0, cplx_to_bit(start)))

    best_score = None
    all_visited = dict()    # score -> bitfield of visited nodes

    while len(queue):
        state = queue.pop()
        if state.p == end:
            if best_score is None:
                all_visited[state.s] = all_visited.get(state.s, 0) | state.v
                best_score = state.s
                print(f"... {best_score} ({len(queue)})")
            else:
                if state.s <= best_score:
                    all_visited[state.s] = all_visited.get(state.s, 0) | state.v
                    if state.s < best_score:
                        best_score = state.s
                        print(f"... {best_score} ({len(queue)})")
            continue
        
        best = best_cache.get((state.p, state.d), None)
        if best is not None and best < state.s:
            continue
        best_cache[(state.p, state.d)] = state.s

        cp = state.copy().try_advance()
        if cp is not None:
            queue.append(cp)

        best = best_cache.get((state.p, state.d*1j), None)
        if best is not None and best < state.s + 1000:
            pass
        else:
            best_cache[(state.p, state.d*1j)] = state.s + 1000
            cp = state.copy().rotate_right().try_advance()
            if cp is not None:
                queue.appendleft(cp)
        
        best = best_cache.get((state.p, state.d*-1j), None)
        if best is not None and best < state.s + 1000:
            pass
        else:
            best_cache[(state.p, state.d*-1j)] = state.s + 1000
            cp = state.copy().rotate_left().try_advance()
            if cp is not None:
                queue.appendleft(cp)
        

    return best_score, all_visited[best_score].bit_count()

def tests():
    assert(work(test_input_1) == (7036, 45))
    assert(work(test_input_2) == (11048, 64))
tests()

def p1_p2():
    print(work(real_input))
p1_p2()
