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

with open("testinput.txt","r") as f:
    example = f.readlines()


## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)

ROWS = len(lines)
COLS = len(lines[0])

def draw_energized(mapin,energized):
    for rnum,r in enumerate(mapin):
        for cnum,c in enumerate(r):
            if (rnum,cnum) not in energized:
                cleanch = c 
                if cleanch == "\\":
                    cleanch = "L"
                p(f"[blue]{cleanch}[/blue]",end="")
            else:
                p(f"[green]#[/green]",end="")
        print()

def normal_move(r,c,rdir,cdir):
    newr = r + rdir
    newc = c + cdir
    if newr >= 0 and newr < ROWS and newc >= 0 and newc < COLS:
        return [((newr,newc),(rdir,cdir))]
    return []

@lru_cache(maxsize=None)
def do_move(r,c,rdir,cdir):
    ch = lines[r][c]
    new_beam_heads = []
    match ch:
        case ".":
            newheads = normal_move(r,c,rdir,cdir)
            for head in newheads:
                # valid, will mark energized next round
                #print(f"[{ch}] @ ({r},{c}) -> moving to ({head})")
                new_beam_heads.append(head)
        case "/":
            match (rdir,cdir):
                case (0,1): # right
                    newrdir = -1 # up
                    newcdir = 0
                case (0,-1): # left
                    newrdir = 1 # down
                    newcdir = 0
                case (1,0): # down
                    newrdir = 0
                    newcdir = -1 # left
                case (-1,0): # up
                    newrdir = 0
                    newcdir = 1 # right
                case _:
                    print(f"ERROR {rdir},{cdir},'{ch}'")
            # now that we've changed directions, treat like "."
            newheads = normal_move(r,c,newrdir,newcdir)
            for head in newheads:
                # valid, will mark energized next round
                #print(f"[{ch}] @ ({r},{c}) -> moving to ({head})")
                new_beam_heads.append(head)
        case "\\":
            match (rdir,cdir):
                case (0,1): # right
                    newrdir = 1 # down
                    newcdir = 0
                case (0,-1): # left
                    newrdir = -1 # up
                    newcdir = 0
                case (1,0): # down
                    newrdir = 0
                    newcdir = 1 # right
                case (-1,0): # up
                    newrdir = 0
                    newcdir = -1 # left
                case _:
                    print(f"ERROR {rdir},{cdir},'{ch}'")
            # now that we've changed directions, treat like "."
            newheads = normal_move(r,c,newrdir,newcdir)
            for head in newheads:
                # valid, will mark energized next round
                #print(f"[{ch}] @ ({r},{c}) -> moving to ({head})")
                new_beam_heads.append(head)
        case "-":
            match (rdir,cdir):
                case (1,0) | (-1,0): # down or up
                    # add left and right -- won't move them this pass to simplify the code
                    #print(f"[{ch}] @ ({r},{c}) SPLIT -> moving to left and right")
                    newheads1 = normal_move(r,c,0,-1)
                    newheads2 = normal_move(r,c,0,1)
                    for head in newheads1+newheads2:
                        # valid, will mark energized next round
                        new_beam_heads.append(head)
                case _: # treat like "."
                    newr = r + rdir
                    newc = c + cdir
                    if newr >= 0 and newr < ROWS and newc >= 0 and newc < COLS:
                        # valid, will mark energized next round
                        new_beam_heads.append(((newr,newc),(rdir,cdir)))
                        #print(f"[{ch}] @ ({r},{c}) -> moving to ({newr},{newc}) dir = ({rdir},{cdir})")
        case "|":
            match (rdir,cdir):
                case (0,-1) | (0,1): # left or right
                    # add up and down -- won't move them this pass to simplify the code
                    #print(f"[{ch}] @ ({r},{c}) SPLIT -> moving to up and down")
                    newheads1 = normal_move(r,c,-1,0)
                    newheads2 = normal_move(r,c,1,0)
                    for head in newheads1+newheads2:
                        # valid, will mark energized next round
                        new_beam_heads.append(head)
                    
                case _: # treat like "."
                    newr = r + rdir
                    newc = c + cdir
                    if newr >= 0 and newr < ROWS and newc >= 0 and newc < COLS:
                        # valid, will mark energized next round
                        new_beam_heads.append(((newr,newc),(rdir,cdir)))
                        #print(f"[{ch}] @ ({r},{c}) -> moving to ({newr},{newc}) dir = ({rdir},{cdir})")
        case _:
            print(f"ERROR {ch}")
    return new_beam_heads

def run_map(startr,startc,startrdir,startcdir):
    beam_heads = [((startr,startc),(startrdir,startcdir))]
    energized = set([(startr,startc)])
    processed_beam_heads = set()
    last_energized = 0
    stable_count = 0
    loop_count = 0
    while len(beam_heads) > 0 and stable_count < 10:
        if len(energized) != last_energized:
            stable_count = 0
        else:
            stable_count += 1
        last_energized = len(energized)
        new_beam_heads = []
        for beamhead in beam_heads:
            ((r,c),(rdir,cdir)) = beamhead
            energized.add((r,c))
            if beamhead not in processed_beam_heads:
                processed_beam_heads.add(beamhead)
                newheads = do_move(r,c,rdir,cdir)
                for head in newheads:
                    new_beam_heads.append(head)
        beam_heads = new_beam_heads
        loop_count += 1
        if loop_count % 1000 == 0:
            ic(loop_count,len(beam_heads))
        #draw_energized(lines,energized)
        #print()
    return len(energized)

startr=0
startc=0
startrdir=0
startcdir=0
most_energized=0
for c in range(COLS):
    en = run_map(0,c,1,0) # down from top
    if en > most_energized:
        most_energized = en 
        startr = 0
        startc = c
        startrdir = 1
        startcdir = 0
        ic(most_energized, startr, startc, startrdir, startcdir)
    en = run_map(ROWS-1,c,-1,0) # up from bottom
    if en > most_energized:
        most_energized = en 
        startr = ROWS-1
        startc = c
        startrdir = -1
        startcdir = 0
        ic(most_energized, startr, startc, startrdir, startcdir)

for r in range(ROWS):
    en = run_map(r,0,0,1) # right from left side
    if en > most_energized:
        most_energized = en 
        startr = r
        startc = 0
        startrdir = 0
        startcdir = 1
        ic(most_energized, startr, startc, startrdir, startcdir)
    en = run_map(r,COLS-1,0,-1) # left from right side
    if en > most_energized:
        most_energized = en 
        startr = r
        startc = COLS-1
        startrdir = 0
        startcdir = -1
        ic(most_energized, startr, startc, startrdir, startcdir)

ic(most_energized, startr, startc, startrdir, startcdir)
# 7741