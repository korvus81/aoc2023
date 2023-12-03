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

example = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".splitlines()

## to test against example
#input = example

lines = [list(l) for l in [s.strip() for s in input]]

digits = set([str(i) for i in range(10)])
nonsymbols = set(['.'] + list(digits))
ic(digits)
ic(nonsymbols)

pp(lines)
symbolpos = []
numpos = []
possible_gearpos = []
for li,l in enumerate(lines):
    for chi,ch in enumerate(l):
        if ch not in nonsymbols:
            symbolpos.append((li,chi))
        if ch == "*":
            possible_gearpos.append((li,chi))

possible_num_pos = set()
for (sympos_r,sympos_c) in possible_gearpos:
    possible_num_pos.add((sympos_r-1,sympos_c-1))
    possible_num_pos.add((sympos_r-1,sympos_c))
    possible_num_pos.add((sympos_r-1,sympos_c+1))
    possible_num_pos.add((sympos_r,sympos_c-1))
    possible_num_pos.add((sympos_r,sympos_c+1))
    possible_num_pos.add((sympos_r+1,sympos_c-1))
    possible_num_pos.add((sympos_r+1,sympos_c))
    possible_num_pos.add((sympos_r+1,sympos_c+1))

partnum_locs = []
for li,l in enumerate(lines):
    nums = re.findall(r'\d+',"".join(l))
    ic(nums)

    m = True
    loc=0
    lstr = "".join(l)
    ic(lstr)
    while m:
        lstr_sub = lstr[loc:]
        ic(lstr_sub)
        m = re.search(r'\d+',lstr[loc:])
        if m:
            #digits.append(m.group(0))
            num = m.group(0)
            valid = False
            ic(li,loc,m.start())
            for i in range(len(num)):
                if (li,loc+m.start()+i) in possible_num_pos:
                    ic((li,loc+m.start()+i))
                    valid = True
            if valid:
                digit_locations = {(li,loc+m.start()+i) for i in range(len(num))}
                print("appending:")
                ic(num)
                partnum_locs.append((int(num),digit_locations))
            loc = loc + m.start() + len(num)
            ic(loc)
            if loc >= len(lstr):
                break

ratios = []
for (gli,gchi) in possible_gearpos:
    places_to_look = set()
    places_to_look.add((gli-1,gchi-1))
    places_to_look.add((gli-1,gchi))
    places_to_look.add((gli-1,gchi+1))
    places_to_look.add((gli,gchi-1))
    places_to_look.add((gli,gchi+1))
    places_to_look.add((gli+1,gchi-1))
    places_to_look.add((gli+1,gchi))
    places_to_look.add((gli+1,gchi+1))
    matches = []
    for pn,locset in partnum_locs:
        if not places_to_look.isdisjoint(locset):
            matches.append(pn)
    if len(matches) == 2:
        ic(matches)
        ratios.append(matches[0]*matches[1])
ic(ratios)
ic(sum(ratios))