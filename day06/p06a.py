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

from functools import reduce

def multiply_list(numbers):
  return reduce(lambda x, y: x * y, numbers, 1)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """Time:      7  15   30
Distance:  9  40  200""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)
times = [int(x) for x in re.findall(r'\d+',lines[0])]
distances = [int(x) for x in re.findall(r'\d+',lines[1])]
ic(times)
ic(distances)
races = list(zip(times,distances))
ic(races)
total_ways = []
for tm,maxdist in races:
    ways = 0

    for chg_time in range(tm):
        speed = chg_time
        remaining_time = tm-chg_time
        dist = remaining_time * speed
        if dist > maxdist:
            ways += 1
    ic(ways)
    total_ways.append(ways)
ic(total_ways)
ic(multiply_list(total_ways))