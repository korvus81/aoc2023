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

def map_range(st_in, len_in, mapin):
    ranges_out = []
    mapind = 0
    while mapind < len(mapin):
        cur_st,cur_ln,cur_dst = mapin[mapind]

        if st_in < cur_st:
            if st_in+len_in <= cur_st:
                # totally before this map starts
                ranges_out.append((st_in,len_in))
                return ranges_out
            else:
                # add the part before this map starts and 
                match_length = cur_st-st_in
                ranges_out.append((st_in,match_length))
                ranges_out.extend(map_range(cur_st,len_in-match_length,mapin))
                return ranges_out

        # I think this has to be true, but keeping it here for clarity        
        if st_in >= cur_st:
            # cases:
            # this map entry is completely before st_in
            if cur_st+cur_ln <= st_in:
                mapind += 1
                continue # this is really the only case that loops
            else: # there is overlap
                match_length = min(cur_ln-(st_in-cur_st), len_in)
                # all of st_in+len_in is inside this mapping
                if match_length == len_in:
                    howfar = st_in - cur_st
                    ranges_out.append((cur_dst + howfar,len_in))
                    return ranges_out # should be done
                else: # partial match
                    howfar = st_in - cur_st
                    ranges_out.append((cur_dst + howfar,match_length)) # mapped part
                    ranges_out.extend(map_range(st_in+match_length,len_in-match_length,mapin))
                    return ranges_out


    ranges_out.append((st_in,len_in))
    return ranges_out


# requre both ranges_in and mapin to be sorted
def map_ranges(ranges_in,mapin):
    ranges_out = []
    for st_in,len_in in ranges_in:
        rngs = map_range(st_in,len_in,mapin)
        for r in rngs:
            ranges_out.append(r)
    return sorted(ranges_out)

def map_seed_ranges(seed_start,seed_len):
    
    soil_ranges = map_ranges([[seed_start,seed_len]],seeds_to_soil)
    fert_ranges = map_ranges(soil_ranges,soil_to_fert)
    water_ranges = map_ranges(fert_ranges,fert_to_water)
    light_ranges = map_ranges(water_ranges,water_to_light)
    temp_ranges = map_ranges(light_ranges,light_to_temp)
    hum_ranges = map_ranges(temp_ranges,temp_to_hum)
    loc_ranges = map_ranges(hum_ranges,hum_to_loc)
    return loc_ranges


lowest_loc = 900000000000
lowest_loc_seed = None
for seed_start,seed_len in seed_ranges:
    ic(seed_start,seed_len)
    loc_ranges = map_seed_ranges(seed_start,seed_len)
    ic(loc_ranges)
    cur_lowest_loc = loc_ranges[0][0] # should be sorted
    if cur_lowest_loc < lowest_loc:
        lowest_loc = cur_lowest_loc
        lowest_loc_seed = seed_start # won't be the exact seed, but something

    # for i in range(seed_len):
    #     cur_iters += 1
    #     if cur_iters % 1000000 == 0:
    #         ic(cur_iters,total_iters, 100.0*cur_iters/total_iters,lowest_loc)
    #     seed = seed_start+i
    #     soil = lookup(seeds_to_soil,seed)
    #     fert = lookup(soil_to_fert,soil)
    #     water = lookup(fert_to_water,fert)
    #     light = lookup(water_to_light,water)
    #     temp = lookup(light_to_temp,light)
    #     hum = lookup(temp_to_hum,temp)
    #     loc = lookup(hum_to_loc,hum)
    #     if loc < lowest_loc:
    #         lowest_loc = loc
    #         lowest_loc_seed = seed

ic(lowest_loc)

# tried 952477129
#       283658805
#       231265819
