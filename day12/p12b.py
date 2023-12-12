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
import pprint

preferredWidth = 220
pptr = pprint.PrettyPrinter(width=preferredWidth)
ic.configureOutput(argToStringFunction=pptr.pformat)
ic.lineWrapWidth = preferredWidth

import re
from itertools import combinations,permutations
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()

## to test against example
input = example

lines = [s.strip().split() for s in input]
lines = [[s,[int(n) for n in nums.split(",")]] for s,nums in lines]
pp(lines)

def getpermutations(line):
    perms = []
    for i,ch in enumerate(line):
        if ch == "?":
            p1 = getpermutations(line[:i]+"."+line[i+1:])
            p2 = getpermutations(line[:i]+"#"+line[i+1:])
            return p1 + p2
    return [line]

# def getperms_fromposs(poss_runs):
#     poss = []
#     if len(poss_runs) > 1:
#         later = getperms_fromposs(poss_runs[1:])
#     else:
#         return poss_runs[0]["possible_runs"]
#     for p in poss_runs[0]["possible_runs"]:
#         if len(p) > 0: # don't append 0-length
#             for l in later:
#                 poss.append(p+l)
#         else: 
#             for l in later:
#                 poss.append(l)
#     return poss

# def getperms_fromposs2(poss_runs, runs):
#     ic(poss_runs,runs)
#     poss = []
#     runs_to_match = runs[:]
#     for pnum,p in enumerate(poss_runs):
#         ic(pnum,p["possible_runs"])
#         for prnum,pr in enumerate(p["possible_runs"]):
#             if len(pr) == 0:
#                 print(f"len(pr)==0, calling with {poss_runs[1:]} and {runs}")
#                 poss.extend(getperms_fromposs2(poss_runs[1:], runs))
#             else:
#                 runs_to_check = runs[:len(pr)]
#                 ic(pr,runs_to_check)
#                 if all(pr[i] == runs_to_check[i] for i in range(len(pr))):
#                     # prefix matches, so continue
#                     print(f"Prefix matched, so checking {poss_runs[1:]} against {runs[len(pr):]}...")
#                     newpos = getperms_fromposs2(poss_runs[1:], runs[len(pr):])
#                     for np in newpos:
#                         print(f"adding {pr+newpos}")
#                         poss.append(pr + newpos)
#                 # else ignore
#     time.sleep(4)
#     return poss

def getperms_fromposs3(poss_runs, runs):
    #ic(poss_runs,runs)
    poss = []
    if len(poss_runs) < 1:
        return []
    p=poss_runs[0]
    #ic(p)
    for prnum,pr in enumerate(p):
        #ic(pr)
        if len(pr) == 0:
            if len(poss_runs) > 1:
                #print(f"len(pr)==0, calling with {poss_runs[1:]} and {runs}")
                res = getperms_fromposs3(poss_runs[1:], runs)
                for r in res:
                    #print(f"Adding {r} from 0 case...")
                    poss.append(r)
                #ic(poss)
            else:
                pass
                #print(f"len(pr)==0, and poss_runs <= 1, so adding nothing")
        else:
            if len(runs) >= len(pr):
                runs_to_check = runs[:len(pr)]
                #ic(pr,runs_to_check)
                if all(pr[i] == runs_to_check[i] for i in range(len(pr))):
                    # prefix matches, so continue
                    if len(runs_to_check) == len(runs) and (len(poss_runs) == 1 or all(() in p for p in poss_runs[1:])):
                        #print(f"Prefix ({pr}) matched, out of runs (runs_to_check={runs_to_check} == runs={runs}), and either no more possibls runs {len(poss_runs[1:])} or all have () in them.  Adding {pr}")
                        poss.append(pr)
                    else:
                        #print(f"Prefix ({pr}) matched, so checking {poss_runs[1:]} against {runs[len(pr):]}...")
                        newpos = getperms_fromposs3(poss_runs[1:], runs[len(pr):])
                        for np in newpos:
                            #ic(np)
                            #print(f"adding {tuple(pr)+tuple(np)}")
                            poss.append(tuple(pr) + tuple(np))
            else:
                pass
                #print(f"len(runs) ({len(runs)}) < len(pr) ({len(pr)}) so not even looking for a match")
            # else ignore
    #print(f"returning {poss}")
    return tuple(poss)

def getpermutations_hint(line,runs):
    largest_run = max(runs)
    largest_run_str = "#"*largest_run
    poss_runs = getpotentialruns(line)
    #ic(line)
    ic(poss_runs)
    poss_runs_raw = [p["possible_runs"] for p in poss_runs]
    ic(poss_runs_raw)
    perms = getperms_fromposs3(poss_runs_raw, runs)
    #ic(perms)
    
    # maybe a first pass helps?
    filtered_perms =[p for p in perms if p[0] == runs[0]]
    filtered_perms =[p for p in filtered_perms if p == tuple(runs)]
    
    #ic(filtered_perms)
    

    return filtered_perms


@lru_cache(maxsize=1024*1024)
def getruns(line):
    runs = []
    current_run = 0
    for i,ch in enumerate(line):
        if ch == ".":
            if current_run > 0:
                runs.append(current_run)
                current_run = 0
            else:
                continue
        elif ch == "#":
            current_run = current_run + 1
    if current_run > 0:
        runs.append(current_run)
        current_run = 0
    return runs

def getpotentialruns(line):
    runs = []
    current_run = 0
    for i,ch in enumerate(line):
        if ch == ".":
            if current_run > 0:
                runstr = line[i-current_run:i]
                perms = getpermutations(runstr)
                possible_runs = [tuple(getruns(p)) for p in perms]
                runs.append({
                    "runlen":current_run,
                    "runstr":runstr,
                    #"definite":all(ch == "#" for ch in runstr),
                    #"perms":perms,
                    "possible_runs":possible_runs})
                current_run = 0
            else:
                continue
        elif ch == "#" or ch == "?":
            current_run = current_run + 1
    if current_run > 0:
        runstr = line[len(line)-current_run:]
        perms = getpermutations(runstr)
        #possible_runs = list(set(tuple(getruns(p)) for p in perms))
        possible_runs = [tuple(getruns(p)) for p in perms]
        runs.append({
            "runlen":current_run,
            "runstr":runstr,
            #"definite":all(ch == "#" for ch in runstr),
            #"perms":perms,
            "possible_runs":possible_runs})
        #runs.append(current_run)
        current_run = 0
    return runs

counts = 0
for linenum,(l,runs) in enumerate(lines):
    # runs = runs of damaged springs
    
    
    # prefix with ? then remove the first
    l = (("?"+l)*5)[1:]
    runs = runs * 5
    ic(linenum,l,runs)

    perms = getpermutations_hint(l,runs)
    ic(len(perms))
    counts += len(perms)
    time.sleep(3)
ic(counts)