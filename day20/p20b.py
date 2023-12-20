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
from dataclasses import dataclass

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a""".splitlines()

example2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output""".splitlines()

## to test against example
#input = example2

def parseline(ln):
    src,dests = ln.split(" -> ")
    src = src.strip()
    dests = dests.strip()
    if src == "broadcaster":
        typ = "b"
        name = src
    elif src[0] == "%" or src[0] == "&":
        typ = src[0]
        name = src[1:]
    else:
        typ = "s" # sink
        name = src
    dests = dests.split(",")
    return {"type":typ,"name":name,"dests":[d.strip() for d in dests]}
    

# @dataclass
# class FlipFlop:
#     name: str
#     state: False # off
#     dests: [str]

#     def receive(self, pulse: bool, src: str):
#         if not pulse:
#             self.state = not self.state




lines = [parseline(s.strip()) for s in input]
modules = {x["name"]:x for x in lines}
pp(lines)
pp(modules)

mod_inputs = {m:[] for m in modules.keys()}
ic(mod_inputs)
for mn in modules.keys():
    for d in modules[mn]["dests"]:
        if d not in mod_inputs: # for things that only show up as destinations
            mod_inputs[d] = []
        mod_inputs[d].append(mn)
ic(mod_inputs)

for mname,m in modules.items():
    if m["type"] == "%":
        m["state"] = False # off
    elif m["type"] == "&":
        m["state"] = {i:False for i in mod_inputs[mname]}
    # ignore others
        
ic(modules)

def push_button(modules,verbose=False):
    pulse_counter = {False:1,True:0}
    sunk_pulses = {False:0,True:0}
    operation_list = [("broadcaster",False,"button")] # module, pulse, source
    while len(operation_list) > 0:
        mname,pulse,src = operation_list.pop(0)
        mod = modules.get(mname,{"type":"s","name":mname,"dests":[]})
        cur_state = mod.get("state",{})
        match mod["type"]:
            case "b": # broadcast
                if verbose:
                    p(f"[cyan]{src: >12}[/cyan] [red]{pulse}[/red]-> \t[green]{mname:14}[/green]")
                for d in mod["dests"]:
                    pulse_counter[pulse] += 1
                    operation_list.append( (d,pulse,mname) )
            case "%": # flip-flop
                if verbose:
                    p(f"[cyan]{src: >12}[/cyan] [red]{pulse}[/red]-> \t[green]{mname:14}[/green] -- Flip-Flop (%) {cur_state}")
                if not pulse: # only respond to low
                    cur_state = modules[mname]["state"]
                    new_state = not cur_state
                    modules[mname]["state"] = new_state
                    for d in mod["dests"]:
                        pulse_counter[new_state] += 1
                        operation_list.append( (d,new_state,mname) )
            case "&": # conjunction
                if verbose:
                    p(f"[cyan]{src: >12}[/cyan] [red]{pulse}[/red]-> \t[green]{mname:14}[/green] -- Conjunction (&) {cur_state}")
                # update first
                modules[mname]["state"][src] = pulse
                tosend = True
                #p([srcstate for srcstate in modules[mname]["state"].values()])
                if all(srcstate for srcstate in modules[mname]["state"].values()):
                    # high for all inputs
                    tosend = False 
                for d in mod["dests"]:
                    pulse_counter[tosend] += 1
                    operation_list.append( (d,tosend,mname) )
            case "s": # sink
                if verbose:
                    p(f"[cyan]{src: >12}[/cyan] [red]{pulse}[/red]-> \t[green]{mname:14}[/green] -- Sink")
                sunk_pulses[pulse] += 1
    return pulse_counter,sunk_pulses

total_pulses = {True:0,False:0}
i = 0
#for i in range(100000000):
while True:
    i += 1
    #print()
    # if i % 100000 == 0:
    #     print(f"=== {i+1}")
    pulses,sunk = push_button(modules, verbose=False) # mutates in place!
    for k,v in pulses.items():
        total_pulses[k] += v
    if (i+1) % 100000 == 0:
        print(f"=== {i+1}")
        ic(pulses)
        ic(sunk)
    if sunk[False] > 0:
        print(f"=== {i+1} pushes!")
        break


ic(total_pulses)
ic(total_pulses[False] * total_pulses[True])
# 925955316