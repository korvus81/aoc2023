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
from itertools import combinations,permutations
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()

## to test against example
#input = example

lines = [s.strip().split() for s in input]
lines = [[s,[int(n) for n in nums.split(",")]] for s,nums in lines]
pp(lines)

def getpermutations(line):
    perms = []
    for i,ch in enumerate(line):
        if ch == "?":
            p1 = getpermutations(line[:i]+"."+line[i+1:])
            p2 = getpermutations(line[:i]+"#"+line[i+1:])
            return p1 + p2
    return [line]

def getruns(line):
    runs = []
    current_run = 0
    for i,ch in enumerate(line):
        if ch == ".":
            if current_run > 0:
                runs.append(current_run)
                current_run = 0
            else:
                continue
        elif ch == "#":
            current_run = current_run + 1
    if current_run > 0:
        runs.append(current_run)
        current_run = 0
    return runs

counts = 0
for l,runs in lines:
    # runs = runs of damaged springs
    print()
    perms = getpermutations(l)
    ic(l)
    #ic(perms)
    for p in perms:
        foundruns = getruns(p)
        if len(foundruns) == len(runs) and all(foundruns[i]==runs[i] for i in range(len(runs))):
            ic(p)
            ic(foundruns)
            counts += 1
ic(counts)
# 6852