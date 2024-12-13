#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys, re

test_input="""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_13"]

real_input = list(fileinput.input())

def parse_inputs(inputs, part2=False):
    re_int = re.compile(r"([0-9]+)")

    machines = []

    idx = 0
    values_a = None
    values_b = None
    values_prize = None
    for line in inputs:
        line = line.strip()
        values = None
        if idx in (0,1,2):
            values = re_int.findall(line)
            values = tuple(map(int, values))
        if idx == 0:
            values_a = values
        if idx == 1:
            values_b = values
        if idx == 2:
            values_prize = values
            if part2:
                values_prize = tuple(map(lambda x:x+10000000000000, values_prize))
            machines.append((values_a, values_b, values_prize))
        idx = (idx + 1) % 4

    return machines

def work(inputs, part2=False):
    machines = parse_inputs(inputs, part2)

    result = 0
    for machine in machines:
        values_a, values_b, values_prize = machine
        # a * D_AX + b * D_BX = X
        # a * D_AY + b * D_BY = Y
        eq1 = (values_a[0], values_b[0], values_prize[0]) # D_AX, D_BX, X
        eq2 = (values_a[1], values_b[1], values_prize[1]) # D_AY, D_BY, Y

        # a * D_AX * D_AY + b * D_BX * D_AY = X * D_AY
        # a * D_AY * D_AX + b * D_BY * D_AX = Y * D_AX
        eq3 = tuple(map(lambda x:x*eq2[0], eq1))
        eq4 = tuple(map(lambda x:x*eq1[0], eq2))
        # b * (D_BX - D_BY) = X * D_AY - Y * D_AX
        diff1 = tuple(x - y for x, y in zip(eq3, eq4))

        # a * D_AX * D_BY + b * D_BX * D_BY = X * D_BY
        # a * D_AY * D_BX + b * D_BY * D_BX = Y * D_BX
        eq5 = tuple(map(lambda x:x*eq2[1], eq1))
        eq6 = tuple(map(lambda x:x*eq1[1], eq2))
        # a * (D_AX - D_AY) = X * D_BY - Y * D_BX
        diff2 = tuple(x - y for x, y in zip(eq5, eq6))

        nb_a, nb_b = None, None
        if diff2[0] != 0 and (diff2[2] % diff2[0] == 0):
            nb_a = diff2[2] // diff2[0]
        if diff1[1] != 0 and (diff1[2] % diff1[1] == 0):
            nb_b = diff1[2] // diff1[1]

        if nb_a is not None and nb_b is not None:
            if part2 or (nb_a <= 100 and nb_b <= 100):
                result += nb_a * 3 + nb_b * 1

    return result

def test_p1():
    assert(work(test_input) == 480)
test_p1()

def p1():
    print(work(real_input))
p1()

def test_p2():
    assert(work(test_input, part2=True) == 875318608908)
test_p2()

def p2():
    print(work(real_input, part2=True))
p2()
