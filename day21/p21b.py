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
from datetime import datetime
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)
from PIL import Image,ImageDraw,ImageFont
import numpy as np
import scipy.misc as smp
from util import *

with open("input.txt","r") as f:
    input = f.readlines()
steps_needed = 26501365

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
#steps_needed=5000

lines = [s.strip() for s in input]
pp(lines)

starting_locations = []
for row,r in enumerate(lines):
    for col,ch in enumerate(r):
        if ch == "S":
            starting_locations.append( (row,col) )
starting_locations = tuple(starting_locations)

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

def printmap_startpath(mapin, starting_locations):
    for row,r in enumerate(lines):
        for col,ch in enumerate(r):
            inpath = False 
            for rs,cs in starting_locations:
                if row == rs or col == cs:
                    inpath = True
            if (row,col) in starting_locations:
                p(f"[magenta]{ch}[/magenta]",end="")
            elif inpath:
                p(f"[red]{ch}[/red]",end="")
            else:
                p(f"[blue]{ch}[/blue]",end="")
        print()                

def render_frame(mapin, starting_locations, grid, steps=0):
    RENDER_ROW_MIN = -2
    RENDER_ROW_MAX = 2
    RENDER_COL_MIN = -2
    RENDER_COL_MAX = 2
    data = np.zeros(((RENDER_ROW_MAX-RENDER_ROW_MIN+1)*ROWS, (RENDER_COL_MAX-RENDER_COL_MIN+1)*COLS, 3)).astype("uint8")
    pixel_row_offset = -1*(RENDER_ROW_MIN*ROWS)
    pixel_col_offset = -1*(RENDER_COL_MIN*COLS)
    counter = 0
    gridcounter = {}
    for gridrow in range(RENDER_ROW_MIN,RENDER_ROW_MAX+1):
        for gridcol in range(RENDER_COL_MIN,RENDER_COL_MAX+1):
            gridcounter[(gridrow,gridcol)] = 0
            g = grid.get((gridrow,gridcol),emptyhash) # default to empty
            dta = grid_cache[g]
            for rownum,rowdta in enumerate(mapin):
                for colnum,coldta in enumerate(rowdta):
                    plot_row = (gridrow*ROWS)+rownum+pixel_row_offset
                    plot_col = (gridcol*COLS)+colnum+pixel_col_offset
                    if gridrow==0 and gridcol==0 and (rownum,colnum) in starting_locations:
                        if (rownum,colnum) in dta:
                            data[plot_row,plot_col] = [255,192,0]
                            counter += 1
                            gridcounter[(gridrow,gridcol)] += 1
                        else:
                            data[plot_row,plot_col] = [255,255,0]
                    elif coldta in ["S","."]:
                        if (rownum,colnum) in dta:
                            data[plot_row,plot_col] = [255,128,128]
                            counter += 1
                            gridcounter[(gridrow,gridcol)] += 1
                        else:
                            data[plot_row,plot_col] = [255,255,255]
                    else:
                        data[plot_row,plot_col] = [192,192,192]
                    if colnum == 0 or rownum == 0:
                        data[plot_row,plot_col] = [255,255,0]
                        
    img = Image.fromarray(data) # mode="RGB"
    scale_factor = 2
    img = img.resize((img.width*scale_factor,img.height*scale_factor))
    d1 = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('DejaVuSansMono-Bold.ttf',32)
    fnt2 = ImageFont.truetype('DejaVuSansMono-Bold.ttf',18)
    
    d1.text((10,img.height-100),f"[{steps}] Total Plots = {counter}",font=fnt, fill=(128, 0, 192))
    for gridrow in range(RENDER_ROW_MIN,RENDER_ROW_MAX+1):
        for gridcol in range(RENDER_COL_MIN,RENDER_COL_MAX+1):
            topleft_row = ((gridrow*ROWS)+pixel_row_offset) * scale_factor
            topleft_col = ((gridcol*COLS)+pixel_col_offset) * scale_factor
            d1.text((topleft_row+10, topleft_col+10),f"In ({gridrow},{gridcol}) = {gridcounter[(gridrow,gridcol)]}",font=fnt2, fill=(0, 0, 192))
    img.save(f"frames/frame_{steps:04d}.png")

#printmap_startpath(lines,starting_locations)
ic(ROWS,COLS)

gardens_in_map = set()
for row,r in enumerate(lines):
        for col,ch in enumerate(r):
            if ch in [".","S"]:
                gardens_in_map.add((row,col))


def fingerprint(locations):
    loc_by_grid = {}
    for r,c in locations:
        localr = r % ROWS
        localc = c % COLS
        gridr = r // ROWS
        gridc = c // COLS
        grid = (gridr,gridc)
        if grid not in loc_by_grid:
            loc_by_grid[grid] = set()
        loc_by_grid[grid].add((localr,localc))
    for grid in sorted(loc_by_grid.keys()):
        locals = tuple(sorted(list(loc_by_grid[grid])))
        localhash = hash(locals)
        print(f"Grid {grid} hash {localhash} ({len(locals)})")

themap = lines

@lru_cache(maxsize=1024*1024*1024)
def get_next_grid(sorted_locs_h, sorted_locs_n_h, sorted_locs_s_h, sorted_locs_e_h, sorted_locs_w_h):
    sorted_locs = grid_cache[sorted_locs_h]
    sorted_locs_n = grid_cache[sorted_locs_n_h]
    sorted_locs_s = grid_cache[sorted_locs_s_h]
    sorted_locs_e = grid_cache[sorted_locs_e_h]
    sorted_locs_w = grid_cache[sorted_locs_w_h]
    next_locs = set()
    for sl in sorted_locs:
        srow,scol = sl
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if themap[r % ROWS][c % COLS] in ["S","."]]
        next_locs = next_locs.union(set(possible))
    for sl in sorted_locs_n:
        srow,scol = sl
        srow = srow - ROWS 
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if themap[r % ROWS][c % COLS] in ["S","."]]
        next_locs = next_locs.union(set(possible))
    for sl in sorted_locs_s:
        srow,scol = sl
        srow = srow + ROWS 
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if themap[r % ROWS][c % COLS] in ["S","."]]
        next_locs = next_locs.union(set(possible))
    for sl in sorted_locs_e:
        srow,scol = sl
        scol = scol + COLS
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if themap[r % ROWS][c % COLS] in ["S","."]]
        next_locs = next_locs.union(set(possible))
    for sl in sorted_locs_w:
        srow,scol = sl
        scol = scol - COLS
        possible = [ (r,c) for (r,c) in [(srow+1,scol),(srow-1,scol),(srow,scol+1),(srow,scol-1)] if themap[r % ROWS][c % COLS] in ["S","."]]
        next_locs = next_locs.union(set(possible))
    next_locs = tuple(sorted([(r,c) for (r,c) in next_locs if r >= 0 and r < ROWS and c >= 0 and c < COLS]))
    #ic(next_locs)
    next_locs_h = hash(next_locs)
    if next_locs_h not in grid_cache:
        grid_cache[next_locs_h] = next_locs
        grid_cache_len[next_locs_h] = len(next_locs)
    return next_locs_h

grid = {(0,0): hash(starting_locations)}

emptyhash = hash(tuple())
grid_cache = {emptyhash: (), hash(starting_locations): starting_locations}
grid_cache_len = {emptyhash:0, hash(starting_locations): len(starting_locations)}

with open("out.txt", "w") as fout:
    startdt = datetime.now()
    for i in range(steps_needed):
        grids = list(grid.keys())
        minrow = 0
        mincol = 0
        maxrow = 0
        maxcol = 0
        for r,c in grids:
            if grid[(r,c)] != emptyhash: # ignore empty
                if r < minrow:
                    minrow = r
                if r > maxrow:
                    maxrow = r
                if c < mincol:
                    mincol = c
                if c > maxcol:
                    maxcol = c
        #ic(grids)
        newgrid = {}
        for gridrow in range(minrow-1,maxrow+2):
            for gridcol in range(mincol-1,maxcol+2):
                g = grid.get((gridrow,gridcol),emptyhash) # default to empty
                gn = grid.get((gridrow-1,gridcol),emptyhash)
                gs = grid.get((gridrow+1,gridcol),emptyhash)
                gw = grid.get((gridrow,gridcol-1),emptyhash)
                ge = grid.get((gridrow,gridcol+1),emptyhash)
                #ic(gridrow,gridcol)
                #ic(g,gn,gs,ge,gw)
                #ic(type(g),type(gn),type(gs),type(ge),type(gw))
                local_pos = get_next_grid(g, gn, gs, ge, gw)
                if grid_cache_len[local_pos] > 0 or grid_cache_len[g] > 0:
                    newgrid[(gridrow,gridcol)] = local_pos
        grid = newgrid
        fout.write(f"{sum(grid_cache_len[v] for v in grid.values())}\n")
        render_frame(lines, starting_locations, grid, steps=i+1)
        if i % 10:
            fout.flush()
        if i % 100 == 0 and i > 0:
            fout.flush()
            ic(i)
            elapsed = datetime.now()-startdt
            ic(datetime.now(),elapsed, elapsed/i)
            ic(grid.keys())
            ic({k:grid_cache_len[v] for k,v in grid.items()})
            ic(sum(grid_cache_len[v] for v in grid.values()))

print("=======")
ic(i)
ic(grid.keys())
ic({k:grid_cache_len[v] for k,v in grid.items()})
ic(sum(grid_cache_len[v] for v in grid.values()))

#pp = possible_plots(lines,starting_locations, steps_needed)
#ic(pp)
#ic(len(pp))
#ic(len(gardens_in_map.difference(pp)))

"""
Notes:
- At step 131 (width/height of puzzle) there are 7282 in the middle, 1889 N, 1879 E, 1909 W, 1919 S.  
  - At this point, we have reached the starting location in all four adjacent grids
  - We are exactly one step before getting into the NE/NW/SE/SW grids
- At step 132, there are 7406 in the middle, and this should keep alternating between 7282 and 7406 forever (even steps = 7282, odd steps = 7409)
- (note that my step count at the bottom in the current iteration is off by 1 -- it says step 130 on frame 131, but I never render a zero frame)
- Theory: at every multiple of 131, all the fully enclosed grids will alternate like the middle (possibly with different numbers?),
- Theory: at every multiple of 131, the four corners will have the same count and 
- Theory: at the desired final step, the edges are in the diamond-shaped open space, making it easier to calculate (I show that around 190-200, and 190%131==59, 200%131==69)
    >>> 26501365 % 131
    65
- Theory: I believe I can calculate the steady state at 202300 * 131, and then extrapolate what it will look like when it goes 65 more steps to the edge
    >>> 26501365 // 131
    202300
- At step 196, NW = 957, NE = 932, SE = 947, SW = 933, 
    - N=5492, S=5489, E=5509, W=5472
    - (and 196 % 131 == 65 AND that is the point just before we break into two grids N/S/E/W)
- Q: At step 262, will the NE/NW/SE/SW quadrants have reliable numbers that always exist when they are diagonally filled?
    - At 262, NW=3743, NE=3722, SE=3747, SW=3789 -- will need to run 131 further to know for sure, and I need a bigger diagram for that.
- Q: At step 262, will N/S/E/W have the same alternating pattern as the center?
    - Yes, except opposite.  When the middle is 7406, the NSEW are 7282 (which is the case at exactly 262), and vice-versa 
- At step 262, we should have just filled the N/S/E/W squares from the origin, and I suspect the second N/S/E/W will look like step 131, with the diagonals being a little question mark
- At 26501365 - 65, we expect to have filled grids that go 202300 tall and 202300 wide in a diamond pattern.
    - The far N/S/E/W squares should look like the squares at step 131
    - at 131*1 we have 1 square, at 131*2 we have 5 squares, at 131*3 we have 13? (2 N/S/E/W of center, 1 in each NW/NE/SE/SW corners from center, plus the center).  At N multiples of 131, we should have 2*(N)^2-2N+1 squares, of which roughly half will be 7406/7282.
    - I believe this means we will have 2*(202300**2) - 2*202300 + 1 = 81850175401 full squares, of which 40925087700 will have one count and 40925087701 will have another (gut feeling, 7406 of the larger and 7282 of the smaller)
    - (202300-1) of each type of diag
    - 4 "corners/points"
    - Maybe the answer is 40925087700*7282 + 40925087701*7406 + 3743*(202300-1) + 3722*(202300-1) + 3747*(202300-1) + 3789*(202300-1) + <scratch this, that was before we add the extra 65>
    - on frame_0327, N=2, we have two small (957/932/947/933) and one large (6372/6402/6389/6382) segments on diag
        - I think at N=3, we will have SLSLS so 3 small, 2 large on each edge.  I think we always have N small an N-1 large?
    - full_squares = 40925087700*7282 + 40925087701*7406
    - full_squares = 40925087701*7282 + 40925087700*7406 # based on frame_0327, which is also an even N
    - points = 5472 + 5492 + 5509 +  5489 # from frame_0196
    - diag = (957+932+947+933) * (202300-1) # from frame_0196
    - diag = ((957+932+947+933) * 202300) + ((6372+6402+6389+6382) * (202300-1)) # from frame_0327, because they alternate large and small!
    - total = full_squares + points + diag
- Let's try to make a general formula and test it on ones I know (that ideally are 65 when mod 131)
def calc(steps):
    assert (steps % 131) == 65
    if steps % 2 == 0:
        odd = False
    else:
        odd = True
    N = steps // 131 # full grids covered
    if odd:
        full_squares = (N**2-N+1)*7282 + (N**2-N)*7406
    else:
        full_squares = (N**2-N)*7282 + (N**2-N+1)*7406
    points = 5472 + 5492 + 5509 +  5489 # only applies if steps % 131 == 65!
    diag = diag = ((957+932+947+933) * N) + ((6372+6402+6389+6382) * (N-1))
    total = full_squares + points + diag
    return total
>>> calc(196)
33137 # matches!
>>> calc(327)
91703 # I get 91951 in my code :(
At N=2 (327 is odd), frame_0327 shows 4x7406 and 1x7282 square.  That's (N**2)*7406 + ((N-1)**2)*7282 so maybe:
if odd:
    full_squares = ((N-1)**2)*7282 + (N**2)*7406
else:
    full_squares = (N**2)*7282 + ((N-1)**2)*7406

    New version:
def calc(steps):
    assert (steps % 131) == 65
    if steps % 2 == 0:
        odd = False
    else:
        odd = True
    N = steps // 131 # full grids covered
    if odd:
        full_squares = ((N-1)**2)*7282 + (N**2)*7406
    else:
        full_squares = (N**2)*7282 + ((N-1)**2)*7406
    points = 5472 + 5492 + 5509 +  5489 # only applies if steps % 131 == 65!
    diag = diag = ((957+932+947+933) * N) + ((6372+6402+6389+6382) * (N-1))
    total = full_squares + points + diag
    return total

Based on testing, I think I might have this even/odd thing off.
def calc(steps):
    assert (steps % 131) == 65
    N = steps // 131 # full grids covered
    full_squares = ((N-1)**2)*7282 + (N**2)*7406
    points = 5472 + 5492 + 5509 +  5489 # only applies if steps % 131 == 65!
    diag = diag = ((957+932+947+933) * N) + ((6372+6402+6389+6382) * (N-1))
    total = full_squares + points + diag
    return total
>>> calc(196)
33137 # match!
>>> calc(327)
91951 # match! 
>>> calc(26501365)
601113643448699
"""
# 601117734921705 is too high
# 601108450631899 is too low
# 601113618363499 is too low
# 601113618363623 is "not the right answer"
# 601113643448699 CORRECT!!!!!