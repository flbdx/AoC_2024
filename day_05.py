#!/usr/bin/python3
#encoding: UTF-8

import fileinput
import sys

test_input="""47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".splitlines()

if len(sys.argv) == 1:
    sys.argv += ["input_05"]

real_input = list(fileinput.input())

def ordering_is_good(rules, pages):
    for a, before in rules.items():
        if a not in pages:
            continue
        for b in before:
            if not b in pages:
                continue
            if pages[a] >= pages[b]:
                return a, b # returns wrong pair if the pages are not ordered
            
    return True # else returns True

def work_p1(inputs):
    rules = {}
    ret = 0

    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break
        a, b = line.split("|")
        a, b = int(a), int(b)
        rules.setdefault(a, set()).add(b)
    
    while True:
        try:
            line = next(it)
        except:
            break
        line = line.strip()
        if len(line) == 0:
            break

        pages_list = list(map(int, line.split(",")))
        pages = {}
        for idx, page in enumerate(pages_list):
            pages[page] = idx
        
        if ordering_is_good(rules, pages) == True:
            ret += pages_list[len(pages_list)//2]

    return ret

def work_p2(inputs):
    rules = {}
    ret = 0

    it = iter(inputs)
    while True:
        line = next(it)
        line = line.strip()
        if len(line) == 0:
            break
        a, b = line.split("|")
        a, b = int(a), int(b)
        rules.setdefault(a, set()).add(b)
    
    while True:
        try:
            line = next(it)
        except:
            break
        line = line.strip()
        if len(line) == 0:
            break

        pages_list = list(map(int, line.split(",")))
        pages = {}
        for idx, page in enumerate(pages_list):
            pages[page] = idx
        
        r = ordering_is_good(rules, pages)
        if r == True:
            continue

        while r != True:
            a, b = r
            idxa, idxb = pages[a], pages[b]
            pages[a], pages[b] = pages[b], pages[a]
            pages_list[idxa], pages_list[idxb] = pages_list[idxb], pages_list[idxa]
            r = ordering_is_good(rules, pages)
        ret += pages_list[len(pages_list)//2]
    
    return ret

def test_p1():
    assert(work_p1(test_input) == 143)
test_p1()

def p1():
    print(work_p1(real_input))
p1()

def test_p2():
    assert(work_p2(test_input) == 123)
test_p2()

def p2():
    print(work_p2(real_input))
p2()
