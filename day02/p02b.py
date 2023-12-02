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

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """
""".splitlines()

## to test against example
# input = example

def parse(s):
    parts = s.split(",")
    res = {}
    for part in parts:
        num,color = part.strip().split(" ")
        num = int(num)
        color = color.strip()
        res[color] = num
    return res

lines = [s.strip().split(":")[1].strip().split(";") for s in input]
lines = [[parse(x) for x in l] for l in lines]
pp(lines)

powersum = 0
for i,g in enumerate(lines):
    gamenum = i + 1
    fewest = {"blue":0,"green":0,"red":0}
    for draw in g:
       
        for col in fewest.keys():
            if draw.get(col,0) > fewest[col]:
                fewest[col] = draw.get(col,0)
    pow = 1
    for counts in fewest.values():
        pow = pow * counts
    powersum += pow
print(powersum)