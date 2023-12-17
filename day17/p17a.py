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
from enum import Enum
from util import *

class Dir(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
DIRECTIONS = [Dir.UP,Dir.DOWN,Dir.LEFT,Dir.RIGHT]

with open("input.txt","r") as f:
    input = f.readlines()

example = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)
themap = [[int(ch) for ch in l] for l in lines]
pp(themap)

ROWS = len(lines)
COLS = len(lines[0])

# can move at most 3 times in the same direction
#(row,col),DIR,moves_left
start = ((0,0),Dir.RIGHT,3)
goal = ((ROWS-1,COLS-1),0,0) # last two don't matter

def move_dir(row,col,direction):
    match direction:
        case Dir.UP:
            return (row-1,col)
        case Dir.DOWN:
            return (row+1,col)
        case Dir.LEFT:
            return (row,col-1)
        case Dir.RIGHT:
            return (row,col+1)

@lru_cache(maxsize=None)
def neigh(state):
    neighbors = []
    #ic(state)
    (row,col),d,moves_left = state
    for possd in DIRECTIONS:
        # can't reverse
        if d == Dir.UP and possd == Dir.DOWN or \
            d == Dir.DOWN and possd == Dir.UP or \
            d == Dir.LEFT and possd == Dir.RIGHT or \
            d == Dir.RIGHT and possd == Dir.LEFT:
            #print(f" Can't reverse to {d}")
            continue
        newr,newc = move_dir(row,col,possd)
        if newr < 0 or newc < 0 or newr >= ROWS or newc >= COLS:
            # invalid
            #print(f" {d} off map")
            continue
        elif d == possd: # continuing in same direction
            if moves_left == 0:
                # too many moves in same direction
                #print(f" Can't keep moving straight to {d}")
                continue
            else:
                neighbors.append(((newr,newc),possd,moves_left-1))
        else: # new direction
            neighbors.append(((newr,newc),possd,2)) # 2 more moves
    #ic(state, neighbors)
    return list(neighbors)



# res = astar.find_path(
#     start,
#     goal,
#     neigh,
#     reversePath=False,
#     heuristic_cost_estimate_fnct = lambda a, b: abs(a[0][0]-b[0][0]) + abs(a[0][1]-b[0][1]), # taxicab distance
#     distance_between_fnct = lambda a, b: themap[b[0][0]][b[0][1]], # "cool amount"
#     is_goal_reached_fnct = lambda a, b: a[0][0] == b[0][0] and a[0][1] == b[0][1])

class MyAStar(astar.AStar):
    def __init__(self, themap):
        self.themap = themap


    def neighbors(self, n):
        return neigh(n)

    def distance_between(self, n1, n2):
        return themap[n2[0][0]][n2[0][1]]
            
    def heuristic_cost_estimate(self, current, goal):
        return abs(current[0][0]-goal[0][0]) + abs(current[0][1]-goal[0][1]) # taxicab distance
    
    def is_goal_reached(self, current, goal):
        return current[0] == goal[0] # only compare coords

myas = MyAStar(themap)
res = list(myas.astar(start,goal))
ic(res)
cost = sum([themap[state[0][0]][state[0][1]] for state in res[1:]])
ic(cost)
# 758