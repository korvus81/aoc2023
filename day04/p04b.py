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

example = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
""".splitlines()

## to test against example
#input = example

def parse(line):
    first,second = line.split(":")[1][1:].split("|")
    first = first.strip()
    second = second.strip()
    return [[int(i) for i in first.split()],[int(i) for i in second.split()]]

lines = [s.strip() for s in input]
lines = [parse(line)  for line in lines]
pp(lines)
cards = {(i+1):ln for i,ln in enumerate(lines)}
ic(cards)
cardwins = dict()
total_score = 0
copies = 1
for i,ln in enumerate(lines):
    cardnum = i+1
    win = set(ln[0])
    nums = set(ln[1])
    ic(ln)
    ic(win)
    ic(nums)
    inter = win.intersection(nums)
    if len(inter) == 0:
        cardwins[cardnum] = []
    else:
        cardwins[cardnum] = list(range(cardnum+1,cardnum+len(inter)+1))
        ic(cardnum)
        ic(cardwins)
ic(cardwins)
totalcards = {i:1 for i in cards.keys()}
totalcount = 0
for cardnum in cards.keys():
    num = totalcards[cardnum]
    wins = cardwins[cardnum]
    totalcount += num
    for w in wins:
        totalcards[w] += num
ic(totalcount)