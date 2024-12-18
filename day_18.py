#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from collections import deque

test_input="""5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_18"]

real_input = list(fileinput.input())

def solve(memory, size):
    cplx_to_bit = lambda c : 1<<(int(c.real) + int(c.imag)*size)
    start = 0
    end = size-1 + (size-1) * 1j

    class State:
        def __init__(self, p, s=None, v=None):
            nonlocal cplx_to_bit
            self.p = p
            self.s = 0 if s is None else s
            self.v = cplx_to_bit(p) if v is None else v

        def move(self, direction):
            nonlocal cplx_to_bit, memory
            np = self.p + direction
            if np in memory:
                return False
            if np.real < 0 or np.real >= size or np.imag < 0 or np.imag >= size:
                return False
            if self.v & cplx_to_bit(np):
                return False
            self.p = np
            self.s += 1
            self.v |= cplx_to_bit(self.p)
            return True

        def copy(self):
            return State(self.p, self.s, self.v)

        def __repr__(self):
            return f"{(int(self.p.real), int(self.p.imag))}, {self.s}, {bin(self.v)}"

    queue = deque()
    queue.append(State(start))
    
    best_score = 0xFFFFFFFFFFFFFFFF
    best_cache = {start: 0}
    best_visited = None

    while len(queue):
        s = queue.pop()
        if s.p == end:
            if s.s < best_score:
                best_score = s.s
                best_visited = s.v
            continue

        for d in (1, -1, 1j, -1j):
            ns = s.copy()
            if not ns.move(d):
                continue

            best = best_cache.get(ns.p, None)
            if best is None or best > ns.s:
                best_cache[ns.p] = ns.s
                queue.appendleft(ns)

    return best_score, best_visited


def work_p1(inputs, size, limit):
    memory = set()

    it = iter(inputs)
    for i in range(limit):
        line = next(it).strip()
        x, y = map(int, line.split(','))
        memory.add(x + y*1j)
    
    best_score, best_visited = solve(memory, size)

    return best_score

def work_p2(inputs, size, from_byte):
    memory = set()

    it = iter(inputs)
    for i in range(from_byte):
        line = next(it).strip()
        x, y = map(int, line.split(','))
        memory.add(x + y*1j)
    
    best_score, best_visited = solve(memory, size)

    cplx_to_bit = lambda c : 1<<(int(c.real) + int(c.imag)*size)

    for line in it:
        line = line.strip()
        x, y = map(int, line.split(','))
        p = x + y*1j
        memory.add(p)

        if best_visited & cplx_to_bit(p):
            best_score, best_visited = solve(memory, size)
            if best_visited is None:
                return f"{int(p.real)},{int(p.imag)}"

def test_p1():
    assert(work_p1(test_input, 7, 12) == 22)
test_p1()

def p1():
    print(work_p1(real_input, 71, 1024))
p1()

def test_p2():
    assert(work_p2(test_input, 7, 12) == "6,1")
test_p2()

def p2():
    print(work_p2(real_input, 71, 1024))
p2()
