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

test_area_x_min = 200000000000000
test_area_x_max = 400000000000000


example = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""".splitlines()

## to test against example
#input = example
#test_area_x_min = 7
#test_area_x_max = 27


test_area_y_min = test_area_x_min
test_area_y_max = test_area_x_max

def parse(l):
    pos,vel = l.split("@")
    pos = [int(p.strip()) for p in pos.strip().split(",")]
    vel = [int(v.strip()) for v in vel.strip().split(",")]
    return (tuple(pos),tuple(vel))

lines = [parse(s.strip()) for s in input]
pp(lines)

# vel[1]/vel[0] is delta y over delta x or slope
#data = [(pos,vel,vel[1]/vel[0]) for pos,vel in lines]

def getrange(pos,vel,area_minx,area_maxx):
    pos_x,pos_y,pos_z = pos
    vel_x,vel_y,vel_z = vel
    if vel_x == 0:
        if vel_y > 0:
            miny = pos_y
            maxy = math.inf
        elif vel_y == 0:
            miny = pos_y
            maxy = pos_y
        else: # vel_y < 0
            maxy = pos_y
            miny = math.inf
        return pos_x,pos_x,miny,maxy,math.inf # not moving in X-axis
    slope = float(vel_y)/float(vel_x)
    if vel_x > 0:
        # if moving right, we care from the start of the test area OR the current position, whichever is further right
        minx = max(pos_x,area_minx)
        if minx > area_maxx:
            return None,None,None,None,slope # no intersection possible
        maxx = area_maxx
        if minx == pos_x:
            ystart = pos_y
        else:
            ystart = pos_y + (minx-pos_x)*slope

        yend = pos_y + (area_maxx-pos_x)*slope 
    elif vel_x < 0:
        # if moving left, we care from the max of the test area OR the current position, whichever is further left
        maxx = min(pos_x,area_maxx)
        if maxx < area_minx:
            return None,None,None,None,slope # no intersection possible
        minx = area_minx
        if maxx == pos_x:
            yend = pos_y
        else:
            yend = pos_y + (maxx-pos_x)*slope

        ystart = pos_y + (area_minx-pos_x)*slope 
    return minx,maxx,min(ystart,yend),max(ystart,yend),slope

def intersects(arange_minx,arange_maxx,arange_miny,arange_maxy, arange_slope, brange_minx,brange_maxx,brange_miny,brange_maxy,brange_slope):
    if arange_minx is None or brange_minx is None:
        return False # one of the ranges was invalid
    if arange_maxx < brange_minx or brange_maxx < arange_minx:
        # no overlap in x-coordinates
        return False
    if arange_maxy < brange_miny or brange_maxy < arange_miny:
        # no overlap in y-coordinates
        return False
    if arange_slope == brange_slope:
        #parallel lines
        return False 
    return True # any other cases I need to handle?


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
    # m_a*x + b_a = m*x_b + b_b
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