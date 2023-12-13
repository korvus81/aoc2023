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
#pp(lines)
maps = []
last = 0
for li,l in enumerate(lines):
    if len(l.strip()) == 0:
        maps.append(lines[last:li])
        last=li+1
maps.append(lines[last:])
#ic(maps)

def find_reflection(mapin,ignore_row=None,ignore_col=None):
    cols = len(mapin[0])
    rows = len(mapin)
    # look below rownum for possible reflection
    for rownum in range(rows-1):
        rows_on_top = rownum + 1
        rows_on_bottom = rows-rownum-1
        rows_to_check = min(rows_on_top,rows_on_bottom)
        if False and rownum == 0:
            ic(rownum,rows_on_top,rows_on_bottom,rows_to_check)
       
        rows_above = mapin[rownum+1-rows_to_check:rownum+1][::-1]
        rows_below = mapin[rownum+1:rownum+rows_to_check+1]
        if False and rownum == 0:
            ic(rows_above)
            ic(rows_below)
        if all(rows_above[i] == rows_below[i] for i in range(rows_to_check)):
            if rownum != ignore_row:
                print(f"row reflection at {rownum}")
                return rownum,None
            else:
                pass
                #print(f"ignoring match at row={rownum}")
    
    mapin_t = list(zip(*mapin))
    # look to the right of colnum for possible reflections
    for colnum in range(cols-1):
        cols_to_left = colnum + 1
        cols_to_right = cols-colnum-1
        cols_to_check = min(cols_to_left,cols_to_right)
        #ic(colnum,cols_to_left,cols_to_right,cols_to_check)

        cols_left = mapin_t[colnum+1-cols_to_check: colnum+1][::-1]
        cols_right = mapin_t[colnum+1:colnum+cols_to_check+1]
        #ic(cols_left)
        #ic(cols_right)
        if all(cols_left[i] == cols_right[i] for i in range(cols_to_check)):
            #print(f"col reflection at {colnum}")
            if colnum != ignore_col:
                return None,colnum
            else:
                pass
                #print(f"ignoring match at col={colnum}")

    return None,None

flip_map = {".":"#", "#":"."}

def flip_row(rowin,col):
    return rowin[:col] + flip_map[rowin[col]] + rowin[col+1:]

def flip_map_at(mapin,row,col):
    return mapin[:row] + [flip_row(mapin[row],col)] + mapin[row+1:]

def find_reflection_with_smudge(m):
    oldrow,oldcol = find_reflection(m)
    ic(oldrow,oldcol)
    #total_score += score
    cols = len(m[0])
    rows = len(m)
    for r in range(rows):
        for c in range(cols):
            m2 = flip_map_at(m,r,c)
            #ic(r,c,m2)
            row_found,col_found = find_reflection(m2,ignore_row=oldrow,ignore_col=oldcol)
            if row_found is not None:
                #ic(r,c,row_found)
                return 100 * (row_found + 1)
            if col_found is not None:
                #ic(r,c,col_found)
                return col_found + 1
            

total_score = 0
for m in maps:
    score = find_reflection_with_smudge(m)
    ic(score)
    total_score += score
    print()
ic(total_score)
# 42996