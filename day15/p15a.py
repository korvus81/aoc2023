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

example = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7""".splitlines()

## to test against example
#input = example

lines = [s.strip() for s in input]
pp(lines)
data = "".join(lines).split(",")
pp(data)

def hashalg(st):
    curval = 0
    for i,ch in enumerate(st):
        ac = ord(ch)
        curval += ac
        curval = curval * 17
        curval = curval % 256
    return curval 

#ic(hashalg("HASH"))
ic(sum((hashalg(s) for s in data)))
# 507291