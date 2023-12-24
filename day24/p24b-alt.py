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
pp(lines)


# pts = [(x,y,z,u,v,w) for ((x,y,z),(u,v,w)) in lines]
# xs,ys,zs,us,vs,ws = zip(*pts)
# fig = plt.figure()
# #ax = fig.add_subplot(projection='3d')
# #ax.scatter(xs,ys,zs,marker='o')
# ax2 = fig.add_subplot(projection='3d')
# ax2.quiver(xs,ys,zs,us,vs,ws,length=10000)
# plt.show()
# exit()

# Location for each hailstone is something like:
# (x+(dx*t), y+(dy*t), z+(dz*t))
# t is the only variable
# I need to find a line that intersects them all for some t
# At some t, x+(dx*t) == x_rock+(dx_rock*t)

# For the sample:
# 19, 13, 30 @ -2,  1, -2
# 18, 19, 22 @ -1, -1, -2
# 20, 25, 34 @ -2, -2, -4
# 12, 31, 28 @ -1, -2, -1
# 20, 19, 15 @  1, -5, -3

# 19-2t = x_rock+(dx_rock*t)
#   19-x_rock = (dx_rock+2)*t
# 13+1t = y_rock+(dy_rock*t)
# 30-2t = z_rock+(dz_rock*t)
# for some t > 0.  The t can be different for each hail stone.  
# 7 unknowns and 3 equations.
# but we only add one more unknown with three equations for the next point
# the numpy linear algebra solver wants the form a*x0 + b*x1... = c
# So 19-x_rock = (dx_rock+2)*t0
# (dx_rock+2)*t0 + x_rock = 19 
lines = lines[:5] # takes too long otherwise

x_rock,y_rock,z_rock,dx_rock,dy_rock,dz_rock = sym.symbols("x_rock,y_rock,z_rock,dx_rock,dy_rock,dz_rock")
tvars = sym.symbols(f't:{len(lines)}')
eqs = []
for t in tvars:
    pass
    #eqs.append(sym.Ge(t,0))
for i,(pos,vel) in enumerate(lines):
    pos_x,pos_y,pos_z = pos
    vel_x,vel_y,vel_z = vel
    eqs.append(sym.Eq((dx_rock-vel_x)*tvars[i] + x_rock, pos_x))
    eqs.append(sym.Eq((dy_rock-vel_y)*tvars[i] + y_rock, pos_y))
    eqs.append(sym.Eq((dz_rock-vel_z)*tvars[i] + z_rock, pos_z))
ic(eqs)
vars = tuple(list(tvars)+[x_rock,y_rock,z_rock,dx_rock,dy_rock,dz_rock])
#vars = (x_rock,y_rock,z_rock,dx_rock,dy_rock,dz_rock)
ic(vars)
res = sym.solve(eqs,*vars, dict=True)
#res = sym.nsolve(eqs,vars, (200000000000000, 200000000000000, 200000000000000, 0,0,0), dict=True)
print(res)

# 684195328708898 was the answer with 
# [{dx_rock: 107, dy_rock: -114, dz_rock: 304, t0: 260485297414, t1: 512871273743, t2: 691709521932, t3: 81660418999, t4: 910215709028, x_rock: 242369545669096, y_rock: 339680097675927, z_rock: 102145685363875}]