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
        case "."|"<"|">"|"^"|"v":
            poss = [(r-1,c), (r+1,c), (r,c+1), (r,c-1)]
        # case "<":
        #     poss = [(r,c-1)]
        # case ">":
        #     poss = [(r,c+1)]
        # case "^":
        #     poss = [(r-1,c)]
        # case "v":
        #     poss = [(r+1,c)]
        case _:
            print(f"Error {curch} unknown!")
            exit()
    return list((row,col) for (row,col) in poss if row >= 0 and row < ROWS and col >= 0 and col < COLS and mapin[row][col] != "#")


def get_all_paths(mapin,vertices):
    vertex_to_vertex_map = {}
    vertex_to_vertex_len = {}
    vertex_to_vertex_path = {}

    for v in vertices:
        ic(v)
        vertex_to_vertex_map[v] = []
        startvrow,startvcol = v
        initial_poss = get_possible(v)
        for p in initial_poss:
            ic(p)
            visited = set([v,p])
            cur = p
            path = [cur]
            while cur not in vertices:
                poss = get_possible(cur)
                poss = [p for p in poss if p not in visited]
                #ic(poss)
                cur = poss[0]
                #ic(cur)
                visited.add(cur)
                path.append(cur)
            # found a vertex!
            vertex_to_vertex_map[v].append(cur)
            vertex_to_vertex_len[(v,cur)] = len(path)
            vertex_to_vertex_path[(v,cur)] = path
    
    return vertex_to_vertex_map, vertex_to_vertex_len, vertex_to_vertex_path
            

    

def make_graph(mapin,st):
    vertices = [st]
    for row in range(ROWS):
        for col in range(COLS):
            if mapin[row][col] != "#":
                if len(get_possible((row,col))) > 2:
                    # this must be a fork
                    vertices.append((row,col))
    vertices.append(end)
    #ic(vertices)
    vertex_to_vertex_map, vertex_to_vertex_len, vertex_to_vertex_path = get_all_paths(mapin,vertices )
    return vertices, vertex_to_vertex_map, vertex_to_vertex_len, vertex_to_vertex_path
    
vertices, vertex_to_vertex_map, vertex_to_vertex_len, vertex_to_vertex_path = make_graph(mapin,start)
ic(vertex_to_vertex_map,vertex_to_vertex_len)

def find_all_paths(st,end,vertices,vertex_to_vertex_map, visited=None):
    if visited is None:
        visited = set()
    visited = set(list(visited)) # copy
    visited.add(st)
    #ic(st,visited)
    if st == end:
        return [[end]]
    paths = []
    next_vertices = vertex_to_vertex_map[st]
    for n in next_vertices:
        if n == end:
            paths.append([st,n])
        if n not in visited:
            pths = find_all_paths(n, end, vertices, vertex_to_vertex_map, visited)
            for p in pths:
                #ic(st,p)
                paths.append([st]+p)
    #ic(st,paths)
    return paths

def find_longest_path(st,end,vertices,vertex_to_vertex_map,vertex_to_vertex_len, visited=None):
    if visited is None:
        visited = set()
    else:
        visited = set(list(visited)) # copy
    visited.add(st)
    if st == end:
        return 0,[end] # no further length to go
    #ic(st, vertex_to_vertex_map)
    next_vertices = vertex_to_vertex_map[st]
    longest = -1
    longest_path = []
    for n in next_vertices:
        if n not in visited:
            if False and n == end:
                dist = vertex_to_vertex_len[(st,n)]
                if longest < dist:
                    longest = dist
                    longest_path = [end]
            else:
                dist,pth = find_longest_path(n,end,vertices,vertex_to_vertex_map,vertex_to_vertex_len, visited)
                if dist >= 0:
                    dist += vertex_to_vertex_len[(st,n)]
                    if longest < dist:
                        longest = dist
                        longest_path = pth
    return longest, [st]+longest_path

#paths = find_all_paths(start,end,vertices,vertex_to_vertex_map,vertex_to_vertex_len)
#ic(paths)

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

longest,pth = find_longest_path(start,end,vertices, vertex_to_vertex_map, vertex_to_vertex_len)
ic(pth)
ic(longest)

full_path = set()
for st,end in zip(pth[:-1],pth[1:]):
    steps = vertex_to_vertex_path[(st,end)]
    full_path.update(set(steps))
draw_map(mapin,full_path)
ic(len(full_path))

exit()    

    



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
        # see if this makes it more efficient?
        if len(path) <= 6031:
            return -1,None
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
# 5919 is too low 
# 6422 is the "right answer for someone else"???
# right answer is 6258 !!!!