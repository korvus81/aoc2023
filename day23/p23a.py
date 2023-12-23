#from pprint import pprint as pp 
from rich.pretty import pprint as pp
# https://rich.readthedocs.io/en/latest/markup.html#console-markup
from rich import print as p 
from functools import lru_cache
import os
os.environ["COLUMNS"] = "220" # I usually keep my terminal around 240
import sys
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

sys.setrecursionlimit(20000)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()

example2 = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
#######.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)


ROWS = len(lines)
COLS = len(lines[0])
start = (0,1) #row 0 col 1
end = (ROWS-1,COLS-2)
ic(start,end)

mapin = lines

@lru_cache(maxsize=1024*1024)
def get_possible(st):
    r,c = st
    curch = mapin[r][c]
    
    match curch:
        case ".":
            poss = [(r-1,c), (r+1,c), (r,c+1), (r,c-1)]
        case "<":
            poss = [(r,c-1)]
        case ">":
            poss = [(r,c+1)]
        case "^":
            poss = [(r-1,c)]
        case "v":
            poss = [(r+1,c)]
        case _:
            print(f"Error {curch} unknown!")
            exit()
    return list((row,col) for (row,col) in poss if row >= 0 and row < ROWS and col >= 0 and col < COLS and mapin[row][col] != "#")

def find_path(st,end,curlen=0,path=None,trace=False):
    # if st == (13,21) or st == (17,19) or st == (18,19):
    #     trace = True
    
    if path is None:
        path = []
    path = path[:]
    path.append(st)
    if st == end: # got to the end
        #draw_map(mapin,path)
        ic(len(path))
        return len(path),path
    poss = get_possible(st)

    filtered_poss = [p for p in poss if p not in path]
    
    
    if trace:
        print(f"entering  {st}")
        ic(st,poss,filtered_poss,path)
    poss = filtered_poss
        
    if len(poss) == 0:
        # dead end
        return -1,None

    longest_pth = None
    for p in poss:
        plen,pth = find_path(p,end,curlen+1,path,trace=trace)
        if trace:
            print(f"path found from {st} via {p}")
            ic(p,plen,pth)
        if pth is not None:
            if longest_pth is None or len(pth) > len(longest_pth):
                longest_pth = pth
    if longest_pth is None:
        return -1,None
    #if len(longest_pth) > 90:
    #    ic(longest_pth,len(longest_pth))
    if trace:
        print(f"returning from {st}")
        ic(st,poss,path)
        draw_map(mapin,longest_pth)

    return len(longest_pth),longest_pth

def draw_map(mapin,path):
    p("    ",end="")
    for cnum,ch in enumerate(mapin[0]):
        p(f"{cnum%10}",end="")
    print()
    for rnum,row in enumerate(mapin):
        p(f"{rnum:03d} ",end="")
        for cnum,ch in enumerate(row):
            if (rnum,cnum) in path:
                p(f"[red on yellow]{ch}[/red on yellow]",end="")
            else:
                p(f"[blue]{ch}[/blue]",end="")
        print("")
    print()

plen,pth = find_path(start,end)

ic(pth)
draw_map(mapin,pth)
ic(plen-1)
ic(len(pth)-1)
# 2190