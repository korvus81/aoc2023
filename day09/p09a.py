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
from itertools import pairwise
from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45""".splitlines()

## to test against example
#input = example

lines = [line_to_num_list(s.strip()) for s in input]
pp(lines)

sum_of_vals = 0
for line in lines:
    print()
    lastdiff = 0
    lastvals = [line[-1]]
    ic(line)
    differences = [y-x for x,y in pairwise(line)]
    ic(differences)
    while not all((d == 0 for d in differences)):
        lastvals.append(differences[-1])
        differences = [y-x for x,y in pairwise(differences)]
        ic(differences)
    ic(lastvals)
    last_last_val = 0
    for l in lastvals:
        last_last_val = l+last_last_val
    ic(last_last_val)
    sum_of_vals += last_last_val
ic(sum_of_vals)
# 1980437560