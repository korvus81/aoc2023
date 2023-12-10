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

example3 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L""".splitlines()

## to test against example
#input = example3

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
#ic(dir1_path)
#ic(dir2_path)
ic(len(dir1_path))
ic(len(dir2_path))

def cleanmap(mapin,seen_positions):
    cleanmap = []
    for row,l in enumerate(mapin):
        currow = ""
        for col,ch in enumerate(l):
            if (row,col) in seen_positions:
                currow = currow + ch
            else:
                currow = currow + "."
        cleanmap.append(currow)
    return cleanmap

def drawmap(map,start_row,start_col):
    for row,l in enumerate(map):
        for col,ch in enumerate(l):
            newch = ch.replace("F","\u250C").replace("7","\u2510").replace("-","\u2500").replace("J","\u2518").replace("L","\u2514").replace("|","\u2502")#.replace("."," ")
            if row == start_row and col == start_col:
                p(f"[red]{newch}[/red]",end="")
            elif ch == "?":
                p(f"[bold black]{newch}[/bold black]",end="")
            elif ch == ".":
                p(f"[yellow]{newch}[/yellow]",end="")
            else:
                p(f"[blue]{newch}[/blue]",end="")
        print()

ic(start_row,start_col)
clean = cleanmap(lines,seen_positions=seen_positions)
drawmap(clean,start_row,start_col)

def embiggen(map):
    newmap = []
    lastline = "." * (len(map[0])*2)
    for row,l in enumerate(map):
        newline = ""
        for col,ch in enumerate(l):
            if ch != "-" and ch != "F" and ch != "L": # no path to right
                newline += ch + "?"
            else:
                newline += ch + "-" # to extend the path to the right
        newmap.append(newline)
        # hopefully only leave verticals
        newmap.append(newline.replace("7","|").replace("J","?").replace("L","?").replace("F","|").replace("-","?").replace(".","?"))
        lastline = newline
    return newmap

bigmap = embiggen(clean)
drawmap(bigmap,start_row=start_row*2,start_col=start_col*2)

def get_neightbors(row,col,num_rows,num_cols):
    neighbors = []
    if row > 0:
        neighbors.append((row-1,col))
        if col > 0:
            neighbors.append((row-1,col-1))
        if col < (num_cols-1):
            neighbors.append((row-1,col+1))
    if col > 0:
        neighbors.append((row,col-1))
    if col < (num_cols-1):
        neighbors.append((row,col+1))
    if row < (num_rows-1):
        neighbors.append((row+1,col))
        if col > 0:
            neighbors.append((row+1,col-1))
        if col < (num_cols-1):
            neighbors.append((row+1,col+1))
    return neighbors


def flood_fill_map(map,start_row,start_col):
    # lists lets me individually change elements
    newmap = [[ch for ch in l] for l in map]
    num_rows = len(newmap)
    num_cols = len(newmap[0])
    cleared = set([(0,0)]) # top-left corner is clear
    
    # get the whole border
    for row,l in enumerate(newmap):
        for col,ch in enumerate(l):
            if ch == "." and col == 0 or col == (num_cols-1):
                cleared.add((row,col))


    cleared_can_ignore = set()
    last_cleared_len = 0 # skip the initial check
    while last_cleared_len != len(cleared):
        last_cleared_len = len(cleared)
        for row,col in list(cleared):
            if (row,col) not in cleared_can_ignore:
                coords_to_check = get_neightbors(row,col,num_rows,num_cols)
                cleared_neighbor_count = 0
                for (r,c) in coords_to_check:
                    if newmap[r][c] == "." or newmap[r][c] == "?":
                        newmap[r][c] = " "
                        cleared.add((r,c))
                        cleared_neighbor_count += 1
                    elif newmap[r][c] == " " or (r,c) in cleared:
                        cleared_neighbor_count += 1
                if cleared_neighbor_count == len(coords_to_check):
                    # all neighbors are already cleared, no need to check this again
                    cleared_can_ignore.add((row,col))
    remaining = 0
    for l in newmap:
        for ch in l:
            if ch == ".":
                remaining += 1
    return ["".join(l) for l in newmap],remaining
print()
bigmap_flooded,remaining = flood_fill_map(bigmap, start_row, start_col)
print()
drawmap(bigmap_flooded,start_row*2,start_col*2)

ic(remaining)




