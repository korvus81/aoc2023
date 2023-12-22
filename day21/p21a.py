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
steps_needed = 64

example = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........""".splitlines()

## to test against example
#input = example
#steps_needed=6

lines = [s.strip() for s in input]
pp(lines)

starting_locations = set()
for row,r in enumerate(lines):
    for col,ch in enumerate(r):
        if ch == "S":
            starting_locations.add( (row,col) )

ROWS = len(lines)
COLS = len(lines[0])

def printmap(mapin, possible):
    for row,r in enumerate(lines):
        for col,ch in enumerate(r):
            if (row,col) in possible:
                p(f"[red]O[/red]",end="")
            else:
                p(f"[blue]{ch}[/blue]",end="")
        print()
                


def possible_plots(mapin,starting_locations,steps_needed):
    print()
    ic(steps_needed,starting_locations)
    newsl = set()
    for sl in starting_locations:
        srow,scol = sl
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if r >= 0 and r < ROWS and c >= 0 and c < COLS and mapin[r][c] in ["S","."]]
        #ic(sl,possible)
        newsl = newsl.union(set(possible))
    #ic(steps_needed,newsl)
    #printmap(mapin,newsl)
    if steps_needed == 1:
        return newsl
    else:
        return possible_plots(mapin,newsl,steps_needed-1)

pp = possible_plots(lines,starting_locations, steps_needed)
ic(pp)
ic(len(pp))
# 3637