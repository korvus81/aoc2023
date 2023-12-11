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


galaxies = []
for rownum,row in enumerate(lines):
    for colnum,ch in enumerate(row):
        if ch == "#":
            galaxies.append((rownum,colnum))
ic(galaxies)



def expand_galaxies(mapin,galaxies,factor=1000000):
    startingcols = len(mapin[0])
    emptycols = []
    for col in range(startingcols):
        if all((rowdata[col] == "." for rowdata in mapin)):
            emptycols.append(col)
    ic(emptycols)

    emptyrows = []
    for rownum,row in enumerate(mapin):
        if all((ch == "." for ch in row)):
            emptyrows.append(rownum)
    
    newgalaxies=[]
    for g in galaxies:
        rownum,colnum = g
        # factor -1 because we already counted the row/col once
        # find number of empty rows before this one
        row_ex = (factor-1) * len([row for row in emptyrows if row < rownum])
        # find number of empty columns before this one
        col_ex = (factor-1) * len([col for col in emptycols if col < colnum])
        
        newgalaxies.append((rownum+row_ex,colnum+col_ex))
    return newgalaxies

exgalaxies = expand_galaxies(lines,galaxies=galaxies,factor=1000000)
ic(exgalaxies)

pairs = list(combinations(exgalaxies,2))
#ic(pairs)
ic(len(pairs))

def dist(g1,g2):
    return abs(g1[0]-g2[0])+abs(g1[1]-g2[1])

sum_of_distances = sum([dist(p[0],p[1]) for p in pairs])
ic(sum_of_distances)
# 742305960572
