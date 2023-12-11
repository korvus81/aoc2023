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
from multiprocessing import Pool
# processes_pool = Pool(processes_count)
# processes_pool.map(<function>, <input>)
from itertools import combinations

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....""".splitlines()

## to test against example
#input = example

def printmap(mapin):
    for ln in mapin:
        for ch in ln:
            if ch == "#":
                p(f"[red]{ch}[/red]",end="")
            else:
                p(ch,end="")
        print()
    print()

lines = [s.strip() for s in input]
printmap(lines)

def expand(mapin):
    newmap = []
    startingcols = len(mapin[0])
    emptycols = []
    for col in range(startingcols):
        if all((rowdata[col] == "." for rowdata in mapin)):
            emptycols.append(col)
    ic(emptycols)

    for rownum,row in enumerate(mapin):
        newrow = ""
        lastcol = -1 # I either replace this with 0 or add one
        for col in emptycols:
            if col == 0:
                newrow = newrow + row[0] + "."
                lastcol = 0
                #ic(col,newrow)
            else:
                newrow = newrow + row[lastcol+1:col+1] + "."
                lastcol = col
                #ic(col,newrow)
        if lastcol != (startingcols-1):
            newrow = newrow + row[lastcol+1:]
            #ic(newrow)
        #ic(newrow)
        newmap.append(newrow)
        if all((ch == "." for ch in newrow)):
            newmap.append(newrow)
        #ic(rownum)
        #printmap(newmap)
    return newmap

exmap = expand(lines)
printmap(exmap)

galaxies = []
for rownum,row in enumerate(exmap):
    for colnum,ch in enumerate(row):
        if ch == "#":
            galaxies.append((rownum,colnum))
ic(galaxies)
pairs = list(combinations(galaxies,2))
ic(pairs)
ic(len(pairs))

def dist(g1,g2):
    return abs(g1[0]-g2[0])+abs(g1[1]-g2[1])

sum_of_distances = sum([dist(p[0],p[1]) for p in pairs])
ic(sum_of_distances)
# 9445168