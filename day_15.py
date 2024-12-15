#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input_1="""########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
""".splitlines()

test_input_2="""##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_15"]

real_input = list(fileinput.input())

def read_inputs_p1(inputs):
    walls = set()
    boxes = set()
    bot = None
    max_x = 0
    max_y = 0
    instructions = ""

    it = iter(inputs)
    y = 0
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break

        for x, c in enumerate(line):
            if c == '@':
                bot = x + 1j*y
            elif c == 'O':
                boxes.add(x + 1j*y)
            elif c == '#':
                walls.add(x + 1j*y)
            max_x = max(max_x, x)

        max_y = max(max_y, y)
        y += 1
    
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        instructions += line
    
    return walls, boxes, bot, max_x+1, max_y+1, instructions

def decode(c):
    return {'^': -1j, '>': 1, 'v': 1j, '<': -1}[c]

def work_p1(inputs):
    walls, boxes, bot, width, height, instructions = read_inputs_p1(inputs)

    instructions = list(map(decode, instructions))

    def can_move(p, o):
        np = p + o
        if np in walls:
            return False
        if np in boxes:
            return can_move(np, o)
        return True
    def move_box(p, o):
        np = p + o
        if np in boxes:
            move_box(np, o)
        boxes.remove(p)
        boxes.add(np)

    for inst in instructions:
        if can_move(bot, inst):
            nbot = bot + inst
            if nbot in boxes:
                move_box(nbot, inst)
            bot = nbot

    ret = 0
    for b in boxes:
        ret += 100*int(b.imag) + int(b.real)
    
    return ret

class Box:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def __repr__(self):
        return f"[{self.p1}|{self.p2}]"

def read_inputs_p2(inputs):
    walls = set()
    boxes = dict()
    bot = None
    max_x = 0
    max_y = 0
    instructions = ""

    it = iter(inputs)
    y = 0
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break

        x = 0
        for c in line:
            if c == '@':
                bot = x + 1j*y
                x += 2
            elif c == 'O':
                b = Box(x + 1j*y, x +1 + 1j*y)
                boxes[x + 1j*y] = b
                boxes[x +1 + 1j*y] = b
                x += 2
            elif c == '#':
                walls.add(x + 1j*y)
                walls.add(x +1 + 1j*y)
                x += 2
            else:
                x += 2
            max_x = max(max_x, x)

        y += 1
        max_y = max(max_y, y)
        
    
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        instructions += line
    
    return walls, boxes, bot, max_x, max_y, instructions            

def work_p2(inputs):
    walls, boxes, bot, width, height, instructions = read_inputs_p2(inputs)

    instructions = list(map(decode, instructions))

    def can_move_box(p, o):
        b = boxes[p]
        if o == 1 or o == -1:
            np = b.p2 + o if o == 1 else b.p1 + o
            if np in walls:
                return False
            if np in boxes:
                return can_move_box(np, o)
            return True
        if o == 1j or o == -1j:
            np1 = b.p1 + o
            np2 = b.p2 + o
            if np1 in walls or np2 in walls:
                return False
            if np1 in boxes and np2 in boxes:
                if boxes[np1] == boxes[np2]:
                    return can_move_box(np1, o)
                else:
                    return can_move_box(np1, o) and can_move_box(np2, o)
            if np1 in boxes:
                return can_move_box(np1, o)
            if np2 in boxes:
                return can_move_box(np2, o)
            return True

    def can_move_bot(p, o):
        np = p + o
        if np in walls:
            return False
        if np in boxes:
            return can_move_box(np, o)
        return True
    
    def move_box(p, o):
        b = boxes[p]
        if o == 1:
            np = b.p2 + o
            if np in boxes:
                move_box(np, o)
        if o == -1:
            np = b.p1 + o
            if np in boxes:
                move_box(np, o)
        if o == 1j or o == -1j:
            np1 = b.p1 + o
            np2 = b.p2 + o
            if np1 in boxes and np2 in boxes:
                if boxes[np1] == boxes[np2]:
                    move_box(np1, o)
                else:
                    move_box(np1, o)
                    move_box(np2, o)
            elif np1 in boxes:
                move_box(np1, o)
            elif np2 in boxes:
                move_box(np2, o)

        del boxes[b.p1]
        del boxes[b.p2]
        b.p1 += o
        b.p2 += o
        boxes[b.p1] = b
        boxes[b.p2] = b
        

    for inst in instructions:
        if can_move_bot(bot, inst):
            nbot = bot + inst
            if nbot in boxes:
                move_box(nbot, inst)
            bot = nbot

    ret = 0
    for b in set(boxes.values()):
        ret += 100*int(b.p1.imag) + int(b.p1.real)
    
    return ret

def test_p1():
    assert(work_p1(test_input_1) == 2028)
    assert(work_p1(test_input_2) == 10092)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input_2) == 9021)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
