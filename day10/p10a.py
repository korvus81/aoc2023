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

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """.....
.S-7.
.|.|.
.L-J.
.....""".splitlines()

example2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...""".splitlines()

## to test against example
#input = example2

lines = [s.strip() for s in input]
pp(lines)

def goesto(ch, row=0, col=0):
    match ch:
        case "|":
            return ((row-1,col),(row+1,col))
        case "-":
            return ((row,col-1),(row,col+1))
        case "L":
            return ((row-1,col),(row,col+1))
        case "J":
            return ((row-1,col),(row,col-1))
        case "7":
            return ((row+1,col),(row,col-1))
        case "F":
            return ((row+1,col),(row,col+1))
        case ".":
            return ()
        case _ :
            print(f"ERROR {ch} not known!")
            return

def find_start(lines):
    treat_start_as = "."
    for row,l in enumerate(lines):
        ic(l)
        for col,ch in enumerate(l):
            if ch == "S":
                start_row = row
                start_col = col
                start_pos = (row,col)
                ngoesto = goesto(lines[row-1][col],start_row-1,start_col)
                sgoesto = goesto(lines[row+1][col],start_row+1,start_col)
                egoesto = goesto(lines[row][col+1],start_row,start_col+1)
                wgoesto = goesto(lines[row][col-1],start_row,start_col-1)
                #ic(ngoesto,sgoesto,egoesto,wgoesto)
                if start_pos in ngoesto and start_pos in sgoesto:
                    treat_start_as = "|"
                elif start_pos in ngoesto and start_pos in wgoesto:
                    treat_start_as = "J"
                elif start_pos in ngoesto and start_pos in egoesto:
                    treat_start_as = "L"
                elif start_pos in sgoesto and start_pos in wgoesto:
                    treat_start_as = "7"
                elif start_pos in sgoesto and start_pos in egoesto:
                    treat_start_as = "F"
                elif start_pos in egoesto and start_pos in wgoesto:
                    treat_start_as = "-"
                else:
                    print("Error, can't find what S is!")
                    return
                return (start_row,start_col,treat_start_as)

start_row,start_col,treat_start_as = find_start(lines)
lines = [l.replace("S",treat_start_as) for l in lines]

dir1_path = []
dir2_path = []
seen_positions = set([(start_row,start_col)])

dir1_last,dir2_last = goesto(treat_start_as, start_row, start_col)
while dir1_last not in seen_positions and dir2_last not in seen_positions:
    seen_positions.add(dir1_last)
    seen_positions.add(dir2_last)
    dir1_path.append(dir1_last)
    dir2_path.append(dir2_last)
    dir1_goesto = goesto(lines[dir1_last[0]][dir1_last[1]], dir1_last[0], dir1_last[1])
    dir2_goesto = goesto(lines[dir2_last[0]][dir2_last[1]], dir2_last[0], dir2_last[1])
    if dir1_goesto[0] in seen_positions:
        dir1_last = dir1_goesto[1]
    else:
        dir1_last = dir1_goesto[0]
    if dir2_goesto[0] in seen_positions:
        dir2_last = dir2_goesto[1]
    else:
        dir2_last = dir2_goesto[0]
    #if len(dir1_path) % 1000 == 0:
    #    ic(dir1_path)
    #    ic(dir2_path)
ic(dir1_path)
ic(dir2_path)
ic(len(dir1_path))
ic(len(dir2_path))
