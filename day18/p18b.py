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

example = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)""".splitlines()

## to test against example
#input = example

lines = [re.match(r"([RLUD]) (\d+) \(#([0-9a-f]{6})\)",s.strip()).groups() for s in input]
pp(lines)

# row,col
#trench_coords = [(0,0)] # we will start at 0,0
trench_lines = []
vert_trench_lines = []
horiz_trench_lines = []
cur = (0,0)
for d,stepstr,col in lines:
    #steps = int(stepstr)
    col_steps = col[:5]
    steps = int(col_steps,16)
    #ic(col_steps,steps)
    d = col[-1]
    match d:
        case "U"|"3":
            newpos = (cur[0]-steps,cur[1])
            trench_lines.append((cur,newpos))
            vert_trench_lines.append((cur,newpos))
            cur = newpos
        case "D"|"1":
            newpos = (cur[0]+steps,cur[1])
            trench_lines.append((cur,newpos))
            vert_trench_lines.append((cur,newpos))
            cur = newpos
        case "L"|"2":
            newpos = (cur[0],cur[1]-steps)
            trench_lines.append((cur,newpos))
            horiz_trench_lines.append((cur,newpos))
            cur = newpos
        case "R"|"0":
            newpos = (cur[0],cur[1]+steps)
            trench_lines.append((cur,newpos))
            horiz_trench_lines.append((cur,newpos))
            cur = newpos
ic(trench_lines)
ic(len(trench_lines))
minrow = min(min(r1,r2) for ((r1,c1),(r2,c2)) in trench_lines)
maxrow = max(max(r1,r2) for ((r1,c1),(r2,c2)) in trench_lines)
mincol = min(min(c1,c2) for ((r1,c1),(r2,c2)) in trench_lines)
maxcol = max(max(c1,c2) for ((r1,c1),(r2,c2)) in trench_lines)
ic(minrow,maxrow,mincol,maxcol)

points = [[0,0]]
for ((r1,c1),(r2,c2)) in trench_lines:
    points.append([r2,c2]) # should only appent end of each line -- started with start point

from shapely import Polygon
poly = Polygon(points)
ic(poly)
ic(poly.area)

line_lengths = 0
for ((r1,c1),(r2,c2)) in trench_lines:
    line_lengths += abs(r1-r2) + abs(c1-c2) # one should be 0, 
    # subtract 1 because there will be an overlap for every line, so count start but not the end
ic(line_lengths)
ic(poly.area + line_lengths)
ic(poly.area + (line_lengths/2)+1)

## experimented to figure out how to get the area calculation to match what 
## I'd expect for a rectangle that should have an area of 30...  
## buffer of 0.5 means 0->5 counts as 6 instead of 5 by adding 0.5 to each edge.  
## Not sure why mitre is the right join style, but it worked...
# >>> p=shapely.Polygon([[0,0],[0,4],[5,4],[5,0],[0,0]])
# >>> p
# <POLYGON ((0 0, 0 4, 5 4, 5 0, 0 0))>
# >>> p.area
# 20.0
# >>> p.buffer(0.5)
# <POLYGON ((0 -0.5, -0.049 -0.498, -0.098 -0.49, -0.145 -0.478, -0.191 -0.462...>
# >>> p.buffer(0.5).area
# 29.784137122636483
# >>> p.buffer(0.5,join_style="bevel").area
# 29.5
# >>> p.buffer(0.5,join_style="mitre").area
# 30.0

ic(poly.buffer(0.5,join_style="mitre").area) # <<< this is the one that gives the right answer

## couldn't get these quite right.... but I'm leaving them for posterity
# https://artofproblemsolving.com/wiki/index.php/Shoelace_Theorem
def shoelace_theorem_area(pts):
    summation = 0.0
    for i in range(len(pts)):
        summation += (pts[(i+1) % len(pts)][1] + pts[i][1]) * (pts[(i+1) % len(pts)][0] - pts[i][0])
    return abs(summation)/2

# https://artofproblemsolving.com/wiki/index.php/Pick%27s_Theorem
def picks_theorem_area(points_on_interior,points_on_boundary):
    return points_on_interior + (points_on_boundary/2) -1

sta = shoelace_theorem_area(points)
ic(sta)
pta = picks_theorem_area(sta, line_lengths)
ic(pta)

# 78241949174857 is too low
# 78242031808225 is right
