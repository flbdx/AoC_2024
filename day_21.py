#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
from functools import cache
from collections import deque, namedtuple

test_input="""029A
980A
179A
456A
379A
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_21"]

real_input = list(fileinput.input())

class Keyboard():
    def __init__(self, pad):
        self.key_pos = {}
        self.width = 0
        self.height = 0

        for y, line in enumerate(pad.splitlines()):
            line = line.strip()
            if len(line) == 0:
                break
            for x, c in enumerate(line):
                self.key_pos[c] = x + 1j*y
                self.width = max(self.width, x)
            self.height = max(self.height, y)
        
        self.width += 1
        self.height += 1
    

keypad = Keyboard("""789
                  456
                  123
                  .0A""")

dirpad = Keyboard(""".^A
                  <v>""")

moves = {"^" : -1j, "v" : 1j, "<" : -1, ">" : 1}

@cache
def find_paths(frm, to, pad):
    start = pad.key_pos[frm]
    end = pad.key_pos[to]
    nokey = pad.key_pos["."]

    queue = deque()
    visited = set()
    all_paths = []

    best_score = 1<<64

    State = namedtuple("State", ("p", "s", "path"))

    visited.add(start)
    queue.append(State(start, 0, ""))

    while len(queue) > 0:
        state = queue.pop()
        if state.s > best_score:
            continue
        if state.p == end:
            if state.s < best_score:
                all_paths = []
                best_score = state.s
            all_paths.append(state.path + "A")
        else:
            for c, d in moves.items():
                np = state.p + d
                if int(np.real) < 0 or int(np.real) >= pad.width or int(np.imag) < 0 or int(np.imag) >= pad.height or np == nokey:
                    continue
                if np not in visited:
                    queue.appendleft(State(np, state.s+1, state.path+c))
        visited.add(state.p)
    
    return all_paths

@cache
def solve_for_dirpad(target, robots):
    if robots == 0:
        return len(target)
    
    p = "A"
    total = 0
    for c in target:
        score = 1<<64
        for path in find_paths(p, c, dirpad):
            score = min(score, solve_for_dirpad(path, robots - 1))
        total += score
        p = c
    return total

def solve_for_keypad(target, robots):
    p = "A"
    total = 0
    for c in target:
        score = 1<<64
        for path in find_paths(p, c, keypad):
            score = min(score, solve_for_dirpad(path, robots))
        p = c
        total += score
    
    return total * int(target[:-1])

def work_p1_p2(inputs, robots):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            break
        
        ret += solve_for_keypad(line, robots)
    
    return ret

def test_p1():
    assert(work_p1_p2(test_input, 2) == 126384)
test_p1()

def p1():
    print(work_p1_p2(real_input, 2))
p1()

def test_p2():
    assert(work_p1_p2(test_input, 25) == 154115708116294)
test_p2()

def p2():
    print(work_p1_p2(real_input, 25))
p2()
