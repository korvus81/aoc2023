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
import sympy as sym
from icecream import ic
import re
from itertools import combinations,permutations
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from util import *
import z3

with open("input.txt","r") as f:
    input = f.readlines()



example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""".splitlines()

## to test against example
#input = example



def parse(l):
    pos,vel = l.split("@")
    pos = [int(p.strip()) for p in pos.strip().split(",")]
    vel = [int(v.strip()) for v in vel.strip().split(",")]
    return (tuple(pos),tuple(vel))

lines = [parse(s.strip()) for s in input]
#pp(lines)

x_rock,y_rock,z_rock,dx_rock,dy_rock,dz_rock = z3.Ints("x_rock y_rock z_rock dx_rock dy_rock dz_rock")
tvars = [z3.Int("t"+str(i)) for i in range(len(lines))]
s = z3.Solver()
for i,(pos,vel) in enumerate(lines[:3]):
    pos_x,pos_y,pos_z = pos
    vel_x,vel_y,vel_z = vel
    s.add((dx_rock-vel_x)*tvars[i] + x_rock == pos_x)
    s.add((dy_rock-vel_y)*tvars[i] + y_rock == pos_y)
    s.add((dz_rock-vel_z)*tvars[i] + z_rock == pos_z)

print("checking...")

s.check()
print(s.model())
# [dz_rock = 304,
#  t1 = 512871273743,
#  t3 = 81660418999,
#  dx_rock = 107,
#  dy_rock = -114,
#  t0 = 260485297414,
#  t2 = 691709521932,
#  y_rock = 339680097675927,
#  x_rock = 242369545669096,
#  z_rock = 102145685363875]
print(s.model().evaluate(x_rock+y_rock+z_rock))
# 684195328708898