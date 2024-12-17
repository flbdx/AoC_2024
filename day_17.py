#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import re
from collections import deque

test_input="""Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".splitlines()

test_input_2="""Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".splitlines()


if len(sys.argv) == 1:
    sys.argv += ["input_17"]

real_input = list(fileinput.input())

def pase_inputs(inputs):
    registers = {}
    program = []

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("Register"):
            r = re.match(r"Register ([ABC]): ([0-9]+)", line)
            registers[r.group(1)] = int(r.group(2))
        elif line.startswith("Program"):
            r = re.findall(f"([0-9]+)", line)
            program = list(map(int, r))
    
    return registers, program

class Machine(object):
    def __init__(self, registers, program):
        self.registers = dict(registers)
        self.program = list(program)
        self.registers['I'] = 0
        self.out = []

    class InvalidComboException(Exception):
        pass
    class InvalidOpcodeException(Exception):
        pass

    def combo_reg(self, r):
        if r in (0,1,2,3):
            return r
        if r == 4:
            return self.registers['A']
        if r == 5:
            return self.registers['B']
        if r == 6:
            return self.registers['C']
        raise Machine.InvalidComboException()
    
    def literal_reg(self, r):
        return r
    
    def run(self, debug=False):
        while self.registers['I'] < len(self.program)-1:
            opcode = self.program[self.registers['I']]
            operand = self.program[self.registers['I']+1]

            if opcode == 0: # adv
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | adv {self.registers['A']} // {2**self.combo_reg(operand)} -> {self.registers['A'] // (2**self.combo_reg(operand))}")
                self.registers['A'] = self.registers['A'] // (2**self.combo_reg(operand))
                self.registers['I'] += 2
            elif opcode == 1: # bxl
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | bxl {self.registers['B']} ^ self.literal_reg(operand) -> {self.registers['B'] ^ self.literal_reg(operand)}")
                self.registers['B'] = self.registers['B'] ^ self.literal_reg(operand)
                self.registers['I'] += 2
            elif opcode == 2: # bst
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | bst {self.combo_reg(operand)} & 0b111 -> {self.combo_reg(operand) & 0b111}")
                self.registers['B'] = self.combo_reg(operand) & 0b111
                self.registers['I'] += 2
            elif opcode == 3: # jnz
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | jnz {self.registers['A']} != 0 {self.literal_reg(operand)} -> {self.registers['A'] != 0}")
                if self.registers['A'] == 0:
                    self.registers['I'] += 2
                else:
                    self.registers['I'] = self.literal_reg(operand)
            elif opcode == 4: # bxc
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | bxc {self.registers['B']} ^ {self.registers['C']} -> {self.registers['B'] ^ self.registers['C']}")
                self.registers['B'] = self.registers['B'] ^ self.registers['C']
                self.registers['I'] += 2
            elif opcode == 5: # out
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | out {self.combo_reg(operand) & 0b111}")
                self.out.append(self.combo_reg(operand) & 0b111)
                self.registers['I'] += 2
            elif opcode == 6: # bdv
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | bdv {self.registers['A']} // {2**self.combo_reg(operand)} -> {self.registers['A'] // (2**self.combo_reg(operand))}")
                self.registers['B'] = self.registers['A'] // (2**self.combo_reg(operand))
                self.registers['I'] += 2
            elif opcode == 7: # cdv
                if debug:
                    print(f"{self.registers['I']} | {opcode, operand} | cdv {self.registers['A']} // {2**self.combo_reg(operand)} -> {self.registers['A'] // (2**self.combo_reg(operand))}")
                self.registers['C'] = self.registers['A'] // (2**self.combo_reg(operand))
                self.registers['I'] += 2
            else:
                raise Machine.InvalidOpcodeException()
            if debug:
                print(f"    {self.registers}")

    def get_out(self):
        return ",".join(map(repr, self.out))

def work_p1(inputs):
    registers, program = pase_inputs(inputs)
    
    machine = Machine(registers, program)
    machine.run()
    return machine.get_out()


def work_p2(inputs):
    registers, program = pase_inputs(inputs)
    
    machine = Machine(registers, program)
    machine.run(False)
    target = list(program)

    queue = deque()
    for i in range(8):
        queue.appendleft((i, 1))
    
    result = None
    while len(queue) != 0:
        a, al = queue.pop()
        regs = dict(registers)
        regs['A'] = a
        m = Machine(regs, program)
        m.run()
        if m.out == target[-al:]:
            if al == len(target):
                result = a
                break
            for i in range(7,-1,-1):
                queue.append((i+a*8, al+1))
    
    return result
    


def test_p1():
    assert(work_p1(test_input) == "4,6,3,5,6,3,5,2,1,0")
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input_2) == 117440)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
