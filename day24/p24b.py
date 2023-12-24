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
exit()

def find_intersection(apos,avel, bpos, bvel):
    apos_x,apos_y,apos_z = apos
    bpos_x,bpos_y,bpos_z = bpos
    avel_x,avel_y,avel_z = avel
    bvel_x,bvel_y,bvel_z = bvel
    if avel_x == 0 or bvel_x == 0:
        raise Exception("Haven't handled this case, because I don't think we need to")
    aslope = float(avel_y)/float(avel_x)
    bslope = float(bvel_y)/float(bvel_x)
    if aslope == bslope:
        return None
    aint = apos_y + (0-apos_x) * aslope
    bint = bpos_y + (0-bpos_x) * bslope
    # y_a = m_a*x_a + b_a
    # y_b = m_b*x_b + b_b
    # m_a*x_a + b_a = m_b*x_b + b_b
    # m_a*x -m_b*x =  b_b - b_a
    # (m_a-m_b)*x =  b_b - b_a
    # x =  (b_b - b_a) / (m_a-m_b)
    # then solve for y for either?
    int_x = (bint-aint) / (aslope-bslope)
    int_y = aslope*int_x + aint
    return (int_x,int_y)


count = 0
for (a,b) in combinations(lines,2): #zip(lines[:-1],lines[1:]):
    apos,avel = a
    bpos,bvel = b
    # arange = getrange(apos,avel,test_area_x_min,test_area_x_max)
    # brange = getrange(bpos,bvel,test_area_x_min,test_area_x_max)
    
    # arange_minx,arange_maxx,arange_miny,arange_maxy,arange_slope = arange
    # brange_minx,brange_maxx,brange_miny,brange_maxy,brange_slope = brange
    # inter = intersects(arange_minx,arange_maxx,arange_miny,arange_maxy,arange_slope, brange_minx,brange_maxx,brange_miny,brange_maxy,brange_slope)
    inter = find_intersection(apos,avel,bpos,bvel)
    #ic(a,b,inter)
    if inter:
        interx,intery = inter
        if interx >= test_area_x_min and interx <= test_area_x_max and intery >= test_area_y_min and intery <= test_area_y_max:
            if ((apos[0] < interx and avel[0] > 0) or (apos[0] > interx and avel[0] < 0)) and ((bpos[0] < interx and bvel[0] > 0) or (bpos[0] > interx and bvel[0] < 0)):
                # both are moving toward this point, so let's call it an intersection!
                #print(f"intersects!")
                count += 1
            else:
                pass
                #print(f"don't intersect due to the point being in the past")
        else:
            pass
            #print(f"don't intersect due to being out of area ({interx} not in {test_area_x_min}-{test_area_x_max})")
        
    else:
        pass
        #print(f"don't intersect")
ic(count)
# 26611