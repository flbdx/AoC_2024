#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys
import collections

test_input="""kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_23"]

real_input = list(fileinput.input())

def work_p1(inputs):
    graph = {}

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        a, b = line.split("-")
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    
    all_nodes = set(graph.keys())
    subgraphs = set()
    for n in all_nodes:
        t = (n,)
        subgraphs.add(t)

    for _ in range(2, 4):
        nsubgraphs = set()

        for cur_set in subgraphs:
            tmp = set()
            for n in cur_set:
                tmp.update(graph[n])
            for n2 in tmp:
                connected = True
                for n1 in cur_set:
                    if n2 not in graph[n1]:
                        connected = False
                        break
                if connected:
                    t = tuple(sorted(cur_set + (n2,)))
                    nsubgraphs.add(t)
        
        subgraphs = nsubgraphs
    
    ret = 0
    for s in subgraphs:
        for n in s:
            if n[0] == 't':
                ret += 1
                break
    return ret

def work_p2(inputs):
    graph = {}

    for line in inputs:
        line = line.strip()
        if len(line) == 0:
            continue

        a, b = line.split("-")
        graph.setdefault(a, set()).add(b)
        graph.setdefault(b, set()).add(a)
    
    all_nodes = set(graph.keys())
    subgraphs = set()
    for n in all_nodes:
        t = (n,)
        subgraphs.add(t)

    while True:
        nsubgraphs = set()

        for cur_set in subgraphs:
            tmp = set()
            for n in cur_set:
                tmp.update(graph[n])
            for n2 in tmp:
                connected = True
                for n1 in cur_set:
                    if n2 not in graph[n1]:
                        connected = False
                        break
                if connected:
                    t = tuple(sorted(cur_set + (n2,)))
                    nsubgraphs.add(t)
        
        if len(nsubgraphs) == 0:
            break
        subgraphs = nsubgraphs
    
    return ",".join(subgraphs.pop())

def test_p1():
    assert(work_p1(test_input) == 7)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == "co,de,ka,ta")
test_p2()

def p2():
    print(work_p2(real_input))
p2()
