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

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()

## to test against example
#input = example

lines = [re.match(r"([RLUD]) (\d+) \(#([0-9a-f]{6})\)",s.strip()).groups() for s in input]
pp(lines)

# row,col
trench_coords = [(0,0)] # we will start at 0,0
cur = (0,0)
for d,stepstr,col in lines:
    steps = int(stepstr)
    match d:
        case "U":
            for i in range(steps):
                cur = (cur[0]-1, cur[1])
                trench_coords.append(cur)
        case "D":
            for i in range(steps):
                cur = (cur[0]+1, cur[1])
                trench_coords.append(cur)
        case "L":
            for i in range(steps):
                cur = (cur[0], cur[1]-1)
                trench_coords.append(cur)
        case "R":
            for i in range(steps):
                cur = (cur[0], cur[1]+1)
                trench_coords.append(cur)
ic(trench_coords)
minrow = min(r for r,c in trench_coords)
maxrow = max(r for r,c in trench_coords)
mincol = min(c for r,c in trench_coords)
maxcol = max(c for r,c in trench_coords)
ic(minrow,maxrow,mincol,maxcol)

trench_coords_set = set(trench_coords)

themap = []

# count = 0
# for row in range(minrow,maxrow+1):
#     themap.append("")
#     inside = False
#     currenttrench = False
#     rowcount = 0
#     lasttrench = -1
#     for col in range(mincol,maxcol+1):
#         if (row,col) in trench_coords_set:
#             themap[-1] = themap[-1] + "#"
#             lasttrench = col
#             if not currenttrench: # only toggle if we have seen non-trench
#                 if inside:
#                     inside = False
#                 else:
#                     inside = True
#                     currenttrench = True
#             rowcount += 1 # if we are starting or ending, it's part of the count
#         else:
#             currenttrench = False
#             if inside:
#                 themap[-1] = themap[-1] + "*"
#                 rowcount += 1 # if we have entered the trench but not left a later trench, count it
#             else:
#                 themap[-1] = themap[-1] + "."
#     if inside: # and not currenttrench???
#         # we never exited, so it must have been fake
#         fakerunlen = (col-lasttrench)
#         rowcount -= fakerunlen # if last trench was 10 and col is 15, we remove 5
#         themap[-1] = themap[-1][:-fakerunlen] + ("."* fakerunlen)
#     count += rowcount
#ic(themap)

# let's do a proper flood fill....
#ic([c for r,c in trench_coords if r == minrow])
#ic([c for r,c in trench_coords if r == minrow+1])
# ic| minrow: -233, maxrow: 85, mincol: -107, maxcol: 271
# ic| [c for r,c in trench_coords if r == minrow]: [-48, -47, -46, -45, -44]
# ic| [c for r,c in trench_coords if r == minrow+1]: [-48, -44]
# too lazy to do the math right, so start filling at (-232,-47)

def printmap(minrow,maxrow,mincol,maxcol,trench_coords_set,filled):
    for row in range(minrow,maxrow+1):
        for col in range(mincol,maxcol+1):
            if (row,col) in trench_coords_set:
                p(f"#",end="")
            elif (row,col) in filled:
                p(f"*",end="")
            else:
                p(f".",end="")
        print()

loops = 0
filled = set([(-232,-47)])
#filled = set([(1,2)]) # for example
filled_dont_try = set()
new_filled = True
while new_filled:
    new_filled = False
    if loops % 100 == 0:
        ic(loops, len(filled))
        #printmap(minrow,maxrow,mincol,maxcol,trench_coords_set,filled)
    loops += 1
    for (r,c) in list(filled.difference(filled_dont_try)): # hopefully I can mutate this now....
        for nr,nc in [(r,c+1), (r,c-1), (r+1,c), (r-1,c)]:
            changes = False
            if (nr,nc) not in filled and (nr,nc) not in trench_coords_set:
                filled.add((nr,nc))
                new_filled = True
                changes = True
            if not changes:
                filled_dont_try.add((r,c))


# for row in themap:
#     for col in row:
#         p(f"{col}",end="")
#     print()

printmap(minrow,maxrow,mincol,maxcol,trench_coords_set,filled)
all_coords = filled.union(trench_coords_set)
count = len(filled) + len(trench_coords)
ic(len(filled))
ic(len(trench_coords))
ic(len(all_coords))
ic(count)
# not 52343
# not 41201
# not 39195
# answer was 39194

