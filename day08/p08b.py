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
from icecream import ic
import re
from itertools import cycle
from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
instructions = lines[0]
nodes = lines[2:]
pp(lines)
ic(instructions)
ic(nodes)
def parseline(ln):
    n,rest = ln.split("=")
    n = n.strip()
    l,r = rest.replace("(","").replace(")","").split(",")
    l = l.strip()
    r = r.strip()
    return (n,l,r)


nodes = (parseline(ln) for ln in nodes)
nodes = {n:{"L":l,"R":r} for (n,l,r) in nodes}
ic(nodes)

cur = [n for n in nodes.keys() if n.endswith("A")]
inst = cycle(instructions)
steps = 0
while not all([c.endswith("Z") for c in cur]):
    curinst = inst.__next__()
    cur = [nodes[c][curinst] for c in cur]
    steps += 1
    if steps % 100000 == 0:
        ic(cur,steps)
ic(steps)

