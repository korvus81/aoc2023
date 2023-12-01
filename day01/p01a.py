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
import re

from util import *
#from aocd import lines as lns  # like data.splitlines()
#from aocd import numbers  # uses regex pattern -?\d+ to extract integers from data
#lines = list(lns)
with open("input.txt","r") as f:
    lines = [s.strip() for s in f.readlines()]

pp(lines)
calvalues = []
for l in lines:
    digits = re.findall(r'\d',l)
    print(l)
    pp(digits)
    calvalue = int(digits[0])*10 + int(digits[-1])
    calvalues.append(calvalue)
print(sum(calvalues))

