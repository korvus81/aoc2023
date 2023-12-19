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

def hydrate_rule(rule):
    if ":" not in rule:
        condition = lambda ob: True
        dest = rule
        return {"condition":condition,"dest":dest}
    else:
        c,dest = rule.split(":")
        m = re.match(r"([xmas])([<>])([0-9]+)",c)
        prop = m.group(1)
        comp = m.group(2)
        val = int(m.group(3))
        if comp == "<":
            condition = lambda ob: ob[prop] < val
        elif comp == ">":
            condition = lambda ob: ob[prop] > val
        else:
            print(f"unknown comp {comp} from rule {rule}")
            sys.exit()
        return {"condition":condition,"dest":dest}

def parserule(ln):
    m = re.match(r"(?P<name>[a-z]+)?[{](?P<rules>[^}]+)[}]", ln)
    d = m.groupdict()
    rules = d["rules"].split(",")
    name = d["name"]
    return {"name":name,"rules":[hydrate_rule(r) for r in rules]}

def parseob(ln):
    ln = ln.replace("{","").replace("}","")
    parts = ln.split(",")
    d = {pt.split("=")[0]:int(pt.split("=")[1]) for pt in parts}
    return d

lines = [s.strip() for s in input]
emptyline = lines.index("")
part1,part2 = lines[:emptyline],lines[emptyline+1:]
ic(part1,part2)
part1 = [parserule(l) for l in part1]
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


accepted_obs = []
for ob in obs:
    ic(ob)
    acc = process_ob(ob)
    if acc:
        accepted_obs.append(ob)

ic(accepted_obs)
score = sum(a["x"]+a["m"]+a["a"]+a["s"] for a in accepted_obs)
ic(score)
# 323625


