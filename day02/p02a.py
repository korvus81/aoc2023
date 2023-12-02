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

possiblesum = 0
for i,g in enumerate(lines):
    gamenum = i + 1
    possible = True
    for draw in g:
        if draw.get("red",0) > 12 or draw.get("green",0) > 13 or draw.get("blue",0) > 14:
            possible = False
    if possible:
        possiblesum += gamenum
print(possiblesum)