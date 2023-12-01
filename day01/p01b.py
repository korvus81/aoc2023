#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
os.environ["COLUMNS"] = "220" # I usually keep my terminal around 240
from sys import exit
from collections import defaultdict,namedtuple
import time
from copy import deepcopy
import math 
import astar
import re
from icecream import ic
from util import *
#from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
#lines = list(lns)
with open("input.txt","r") as f:
    lines = [s.strip() for s in f.readlines()]
# lines = [s.strip() for s in """two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen""".splitlines()]

digitmap = {
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9
}


fullre = r'(\d|'+"|".join(list(digitmap.keys()))+ r')'
ic(fullre)
#pp(lines)
calvalues = []

def converttoval(x):
    if x in digitmap:
        return digitmap[x]
    else:
        return int(x)

for l in lines:
    digits = re.findall(fullre,l.lower())
    digits = []
    loc = 0
    m = True
    while m:
        m = re.search(fullre,l[loc:])
        if m:
            digits.append(m.group(0))
            loc = loc + m.pos + 1
            if loc >= len(l):
                break


    print(l)
    pp(digits)
    pp(re.split(fullre,l.lower()))
    calvalue = converttoval(digits[0])*10 + converttoval(digits[-1])
    ic(calvalue)
    calvalues.append(calvalue)
    ic(sum(calvalues))
print(len(calvalues))
#pp(calvalues)
print(sum(calvalues))

