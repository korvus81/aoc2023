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
import sys
from itertools import combinations,permutations
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
""".splitlines()

## to test against example
#input = example

def parse_rule(rule):
    if ":" not in rule:
        dest = rule
        return ("","","",dest)
    else:
        c,dest = rule.split(":")
        m = re.match(r"([xmas])([<>])([0-9]+)",c)
        prop = m.group(1)
        comp = m.group(2)
        val = int(m.group(3))
        return (prop,comp,val,dest)
        
def parserules(ln):
    m = re.match(r"(?P<name>[a-z]+)?[{](?P<rules>[^}]+)[}]", ln)
    d = m.groupdict()
    rules = d["rules"].split(",")
    name = d["name"]
    #return {"name":name,"rules":[hydrate_rule(r) for r in rules]}
    return {"name":name,"rules":[parse_rule(r) for r in rules]}

def parseob(ln):
    ln = ln.replace("{","").replace("}","")
    parts = ln.split(",")
    d = {pt.split("=")[0]:int(pt.split("=")[1]) for pt in parts}
    return d

lines = [s.strip() for s in input]
emptyline = lines.index("")
part1,part2 = lines[:emptyline],lines[emptyline+1:]
ic(part1,part2)
part1 = [parserules(l) for l in part1]
workflows = {wf["name"]:wf["rules"] for wf in part1}
ic(workflows)
obs = [parseob(l) for l in part2]
ic(obs)



def process_ob(ob):
    wflbl = "in"
    wf = workflows[wflbl]
    while True:
        for r in wf:
            if r["condition"](ob):
                dest = r["dest"]
                if dest == "A":
                    return True
                elif dest == "R":
                    return False
                # must be another workflow
                wflbl = dest
                wf = workflows[wflbl]
                break
            else:
                pass # just move to the next rule


# accepted_obs = []
# for ob in obs:
#     ic(ob)
#     acc = process_ob(ob)
#     if acc:
#         accepted_obs.append(ob)

# ic(accepted_obs)
# score = sum(a["x"]+a["m"]+a["a"]+a["s"] for a in accepted_obs)
# ic(score)

MINVAL = 1
MAXVAL = 4000  

state = {k:[(MINVAL,MAXVAL)] for k in "xmas"}
ic(state)

def split_state(statein,prop,op,val):
    propstate = statein[prop]
    propstatetrue = []
    propstatefalse = []
    for minval,maxval in propstate:
        if op == "<":
            if minval < val and maxval < val:
                # whole thing passes
                propstatetrue.append((minval,maxval))
            elif minval > val and maxval > val:
                # whole thing fails
                propstatefalse.append((minval,maxval))
            elif maxval >= val and minval < val:
                # need to split
                propstatetrue.append((minval,val-1))
                propstatefalse.append((val,maxval))
            else:
                print(f"Case I didn't expect {statein} | {prop} | {op} | {val}")
                sys.exit()
        elif op == ">":
            if minval > val and maxval > val:
                # whole thing passes
                propstatetrue.append((minval,maxval))
            elif minval < val and maxval < val:
                # whole thing fails
                propstatefalse.append((minval,maxval))
            elif maxval > val and minval <= val:
                # need to split
                propstatefalse.append((minval,val))
                propstatetrue.append((val+1,maxval))
            else:
                print(f"Case I didn't expect {statein} | {prop} | {op} | {val}")
                sys.exit()
    statetrue = deepcopy(statein)
    statefalse = deepcopy(statein)
    statetrue[prop] = propstatetrue
    statefalse[prop] = propstatefalse
    #ic(statein,prop,op,val)
    #ic(statetrue,statefalse)
    return statetrue,statefalse



def get_states_for_accept(state,rules):
    accept_states = []
    #ic(state,rules)
    if rules[0][0] == "": # always true jump rule
        if rules[0][3] == "R":
            #print(f"REJECT: state: {state}")
            return [] # my input state only rejects
        elif rules[0][3] == "A":
            #print(f"ACCEPT: state: {state}")
            return [state] # my input state only accepts
        else:
            return get_states_for_accept(state,workflows[rules[0][3]])
    st_true,st_false = split_state(state,rules[0][0],rules[0][1],rules[0][2])
    if rules[0][3] == "A":
        #print(f"ACCEPT: state due to {rules[0]}: {st_true}")
        accept_states_true = [st_true]
    elif rules[0][3] == "R":
        #print(f"REJECT: state due to {rules[0]}: {st_true}")
        accept_states_true = [] # all automatically fail
    else:
        accept_states_true = get_states_for_accept(st_true,workflows[rules[0][3]])
    accept_states_false = get_states_for_accept(st_false,rules[1:])
    for ast in accept_states_true:
        accept_states.append(ast)
    for ast in accept_states_false:
        accept_states.append(ast)
    #ic(accept_states_true,accept_states_false,accept_states)
    return accept_states

wflbl = "in"
wf = workflows[wflbl]
sts = get_states_for_accept(state,[("","","","in")])
ic(sts)

count = 0
for st in sts:
    x_ranges = st["x"]
    possible_x = 0
    for rmin,rmax in x_ranges:
        possible_x += rmax-rmin + 1
    
    m_ranges = st["m"]
    possible_m = 0
    for rmin,rmax in m_ranges:
        possible_m += rmax-rmin + 1
    

    a_ranges = st["a"]
    possible_a = 0
    for rmin,rmax in a_ranges:
        possible_a += rmax-rmin + 1

    s_ranges = st["s"]
    possible_s = 0
    for rmin,rmax in s_ranges:
        possible_s += rmax-rmin + 1
    total = possible_x*possible_m*possible_a*possible_s
    ic(possible_x,possible_m,possible_a,possible_s,total)
    count += total 
ic(count)
# answer 127447746739409