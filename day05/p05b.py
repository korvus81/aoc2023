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

example = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".splitlines()

## to test against example
#input = example
#input = [ex+"\n" for ex in example]


#lines = [s.strip() for s in input]
#pp(lines)

parts = "".join(input).split("\n\n")
ic(parts)
ic(len(parts))
seeds,seeds_to_soil,soil_to_fert,fert_to_water,water_to_light,light_to_temp,temp_to_hum,hum_to_loc = parts
seeds = seeds.split(":")[1].strip()
seeds = [int(s) for s in re.findall("\d+",seeds)]
seed_ranges = []
for i in range(int(len(seeds)/2)):
    seed_start = seeds[i*2]
    seed_len = seeds[i*2+1]
    seed_ranges.append((seed_start,seed_len))
seed_ranges.sort()
ic(seed_ranges)

def parse_map(mapstr):
    mlines = mapstr.split(":")[1].strip().splitlines()
    ic(mlines)
    outmap = []
    for ln in mlines:
        dst_start,src_start,rangelen = [int(s) for s in re.findall("\d+",ln)]
        outmap.append((src_start,rangelen,dst_start))
    return sorted(outmap)

def lookup(mapin,val):
    for src_start,rangelen,dst_start in mapin:
        if val >= src_start and val < src_start+rangelen:
            return dst_start+ (val-src_start)
    return val


seeds_to_soil = parse_map(seeds_to_soil)
soil_to_fert = parse_map(soil_to_fert)
fert_to_water = parse_map(fert_to_water)
water_to_light = parse_map(water_to_light)
light_to_temp = parse_map(light_to_temp)
temp_to_hum = parse_map(temp_to_hum)
hum_to_loc = parse_map(hum_to_loc)

total_iters = sum([x[1] for x in seed_ranges])
cur_iters = 0

lowest_loc = 900000000000
lowest_loc_seed = None
for seed_start,seed_len in seed_ranges:
    for i in range(seed_len):
        cur_iters += 1
        if cur_iters % 1000000 == 0:
            ic(cur_iters,total_iters, 100.0*cur_iters/total_iters,lowest_loc)
        seed = seed_start+i
        soil = lookup(seeds_to_soil,seed)
        fert = lookup(soil_to_fert,soil)
        water = lookup(fert_to_water,fert)
        light = lookup(water_to_light,water)
        temp = lookup(light_to_temp,light)
        hum = lookup(temp_to_hum,temp)
        loc = lookup(hum_to_loc,hum)
        if loc < lowest_loc:
            lowest_loc = loc
            lowest_loc_seed = seed

ic(lowest_loc)

# tried 952477129