#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_24"]

real_input = list(fileinput.input())

class Stuff(object):
    def get_value(self, objects:dict):
        raise NotImplementedError()

class Source(Stuff):
    def __init__(self, label:str, value:int, depth=0):
        self.label = label
        self.value = value
        self.depth = depth
        self.op = ""
    
    def get_value(self, objects:dict):
        return self.value
    
    def __repr__(self):
        return f"{self.label}: {self.value}"

class Gate(Stuff):
    def __init__(self, label:str, op:str, src1:str, src2:str):
        self.label = label
        self.value = None
        self.op = op
        self.src1 = src1
        self.src2 = src2
    
    def get_value(self, objects:dict):
        if self.value is not None:
            return self.value
        v = None
        if self.op == "AND":
            v = objects[self.src1].get_value(objects) & objects[self.src2].get_value(objects)
        elif self.op == "OR":
            v = objects[self.src1].get_value(objects) | objects[self.src2].get_value(objects)
        elif self.op == "XOR":
            v = objects[self.src1].get_value(objects) ^ objects[self.src2].get_value(objects)
        self.value = v
        self.depth = max(objects[self.src1].depth, objects[self.src2].depth) + 1
        return v
    
    def __repr__(self):
        return f"{self.src1} {self.op} {self.src2} -> {self.label}"

def work_p1(inputs):
    objects = {}
    outputs = set()

    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break
        label, value = line.split(": ")
        value = int(value)

        objects[label] = Source(label, value)
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        exp, sink = line.split(" -> ")
        src1, op, src2 = exp.split(" ")
        objects[sink] = Gate(sink, op, src1, src2)
        if sink.startswith("z"):
            outputs.add(sink)
    
    s = "".join(repr(objects[z].get_value(objects)) for z in reversed(sorted(outputs)))
    return int(s, base=2)
    

def work_p2(inputs, debug=True):
    objects = {}
    outputs = set()
    inputs_x = set()
    inputs_y = set()

    # manual solving, by printing in an ugly way the gates
    # and searching for incoherencies
    swaps = {
        "z07": "swt", "swt": "z07",
        "rjm": "wsv", "wsv": "rjm",
        "z31": "bgs", "bgs": "z31",
        "z13": "pqc", "pqc": "z13"
    }

    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break
        label, value = line.split(": ")
        value = int(value)

        # we add a depth to each sources and gates used to print the gates 
        objects[label] = Source(label, value, depth=5*int(label[1:]))
        if label.startswith("x"):
            inputs_x.add(label)
        else:
            inputs_y.add(label)
    for line in it:
        line = line.strip()
        if len(line) == 0:
            break
        exp, sink = line.split(" -> ")
        src1, op, src2 = exp.split(" ")
        if not debug:
            sink = swaps.get(sink, sink)
        objects[sink] = Gate(sink, op, src1, src2)
        if sink.startswith("z"):
            outputs.add(sink)
    
    # compute the stuff to assign a depth to each gate
    s = "".join(repr(objects[z].get_value(objects)) for z in reversed(sorted(outputs)))

    if debug:
        # print by ascending depth
        for g in sorted(objects.values(), key=lambda o:(o.depth, o.op)):
            print(f"{g.depth:03d} {g}")
    else:
        sx = "".join(repr(objects[z].get_value(objects)) for z in reversed(sorted(inputs_x)))
        sy = "".join(repr(objects[z].get_value(objects)) for z in reversed(sorted(inputs_y)))
        assert(int(sx, 2) + int(sy, 2) == int(s, 2))
        return ",".join(sorted(swaps.keys()))


def test_p1():
    assert(work_p1(test_input) == 2024)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == None)
# test_p2()

def p2():
    print(work_p2(real_input, debug=False))
p2()
