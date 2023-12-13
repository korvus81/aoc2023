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

example = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)
maps = []
last = 0
for li,l in enumerate(lines):
    if len(l.strip()) == 0:
        maps.append(lines[last:li])
        last=li+1
maps.append(lines[last:])
ic(maps)

def find_reflection(mapin):
    cols = len(mapin[0])
    rows = len(mapin)
    # look below rownum for possible reflection
    for rownum in range(rows-1):
        rows_on_top = rownum + 1
        rows_on_bottom = rows-rownum-1
        rows_to_check = min(rows_on_top,rows_on_bottom)
        ic(rownum,rows_on_top,rows_on_bottom,rows_to_check)
       
        rows_above = mapin[rownum+1-rows_to_check:rownum+1][::-1]
        rows_below = mapin[rownum+1:rownum+rows_to_check+1]
        ic(rows_above)
        ic(rows_below)
        if all(rows_above[i] == rows_below[i] for i in range(rows_to_check)):
            print(f"row reflection at {rownum}")
            return 100*(rownum+1)
    
    mapin_t = list(zip(*mapin))
    # look to the right of colnum for possible reflections
    for colnum in range(cols-1):
        cols_to_left = colnum + 1
        cols_to_right = cols-colnum-1
        cols_to_check = min(cols_to_left,cols_to_right)
        ic(colnum,cols_to_left,cols_to_right,cols_to_check)

        cols_left = mapin_t[colnum+1-cols_to_check: colnum+1][::-1]
        cols_right = mapin_t[colnum+1:colnum+cols_to_check+1]
        ic(cols_left)
        ic(cols_right)
        if all(cols_left[i] == cols_right[i] for i in range(cols_to_check)):
            print(f"col reflection at {colnum}")
            return 1*(colnum+1)

    return 0

total_score = 0
for m in maps:
    score = find_reflection(m)
    ic(score)
    total_score += score
    print()
ic(total_score)
# 31877