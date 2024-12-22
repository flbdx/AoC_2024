#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input_1="""1
10
100
2024
""".splitlines()

test_input_2="""1
2
3
2024
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_22"]

real_input = list(fileinput.input())

class Prng(object):
    def __init__(self, seed):
        self.state = seed
    def run_1(self):
        self.state = (self.state ^ (self.state << 6)) & 0xFFFFFF
        self.state = (self.state ^ (self.state >> 5)) & 0xFFFFFF
        self.state = (self.state ^ (self.state << 11)) & 0xFFFFFF
        return self.state
    def run_n(self, n):
        for _ in range(n):
            self.state = (self.state ^ (self.state << 6)) & 0xFFFFFF
            self.state = (self.state ^ (self.state >> 5)) & 0xFFFFFF
            self.state = (self.state ^ (self.state << 11)) & 0xFFFFFF
        return self.state
    def get_state(self):
        return self.state

def work_p1(inputs):
    ret = 0
    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        s = int(line)
        p = Prng(s)
        ret += p.run_n(2000)
    return ret

def work_p2(inputs):

    all_first_for_sequence = []

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        s = int(line)
        p = Prng(s)

        sequence = list(bytearray(2000+1))
        sequence[0] = s%10
        for i in range(2000):
            sequence[i+1] = p.run_1() % 10
        
        diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]

        first_for_sequence = {}
        for i in range(len(diffs) - 4):
            seq = tuple(diffs[i:i+4])
            v = sequence[i+4]
            first_for_sequence.setdefault(seq, v)

        all_first_for_sequence.append(first_for_sequence)
    
    all_sequences = set()
    for s in all_first_for_sequence:
        all_sequences.update(s.keys())
    
    best_score = 0
    for seq in all_sequences:
        score = sum(l.get(seq, 0) for l in all_first_for_sequence)
        if score > best_score:
            best_score = score
    
    return best_score
        


def test_p1():
    assert(work_p1(test_input_1) == 37327623)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input_2) == 23)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
