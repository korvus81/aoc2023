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

def display_state(modules):
    state = [] 
    for mname in sorted(modules.keys()): #sorted(["fx","lq","ps","js","lm", "jj","hl","tl"]):
        st = modules[mname].get("state")
        if st is not None:
            state.append({mname:st})
    #p(state)
    state = [] 
    #for mname in ["qz","cq","jx","qn","tt","kx","zd","zq","mt"]:   #["zq","kx","mt","qn"]: #sorted(["fx","lq","ps","js","lm", "jj","hl","tl"]):
    for mname in ["qn","kx","zd","zq","mt"]:
        st = modules[mname].get("state")
        if st is not None:
            bool_to_bin = {False:0,True:1}
            cst = {n:bool_to_bin[v] for n,v in st.items()}
            state.append({mname:cst})
    p(state)

def push_button(modules,verbose=False,runnum=0):
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
                if mname in ["kx","mt","zq","zd"] and not tosend:
                    p(f"[{runnum}] {mname} sending {tosend}!")
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
end_states = []
#for i in range(100000000):
while True:
    i += 1
    #print()
    # if i % 100000 == 0:
    #     print(f"=== {i+1}")
    pulses,sunk = push_button(modules, verbose=False,runnum=i) # mutates in place!
    
    tmpstate = []
    for node in ["qz","tt","jx","cq"]:
        tmpstate.append((node,tuple(modules[node]["state"].items())[0]))
    if len(end_states) > 0:
        laststate = end_states[-1]
        for stind,st in enumerate(tmpstate):
            k,v = st
            if st != laststate[stind]:
                print(f"{k} toggled from {laststate[k]} -> {st} at {i}")
    end_states.append(tmpstate)
    
    bool_to_bin = {False:0,True:1}
    # kxin = [bool_to_bin[modules[m]["state"]] for m in ["rm","vg","qt","mp","hd","df","tc","zn","ld","xm","sp","gc"]]
    # if all(x==0 for x in kxin):
    #     print(i,"kx",kxin)
    # if all(x==1 for x in kxin):
    #     print(i,"kx",kxin)
    # #print(i,"kx",kxin)
    

    # mtin = [bool_to_bin[modules[m]["state"]] for m in ["lz","sm","hf","nr","zm","jt","mh","hb","cg","md","gm","gd"]]
    # if all(x==0 for x in mtin):
    #     print(i,"mt",mtin)
    # if all(x==1 for x in mtin):
    #     print(i,"mt",mtin)
    # #print(i,"mt",mtin)

    # zqcnt = [bool_to_bin[modules[m]["state"]] for m in ["fx","lq","js","ps","mb","lm","hc","ls","ql","jj","hl","tl"]]
    # zqin = [bool_to_bin[modules[m]["state"]] for m in ["fx","lq","js","ps","lm","jj","hl","tl"]]
    # if all(x==0 for x in zqin):
    #     print(i,"zq",zqin)
    # if all(x==1 for x in zqin):
    #     print(i,"zq",zqin)
    # #print(i,"zq",zqin)

    # zdin = [bool_to_bin[modules[m]["state"]] for m in ["cl","qc","fs","qs","bz","vj","zk","sq","lf","kg","ph","zb"]]
    # if all(x==0 for x in zdin):
    #     print(i,"zd",zdin)
    # if all(x==1 for x in zdin):
    #     print(i,"zd",zdin)
    # #print(i,"zd",zdin)
    
    #print(f"=== {i}")
    
    #ic(tmpstate)
    

    
    
    #display_state(modules)
    for k,v in pulses.items():
        total_pulses[k] += v
    if (i+1) % 100000 == 0:
        print(f"=== {i+1}")
        ic(pulses)
        ic(sunk)
        #pp(end_states)
    if sunk[False] > 0:
        print(f"=== {i} pushes!")
        break


ic(total_pulses)
ic(total_pulses[False] * total_pulses[True])

# [3907] zd sending False!
# [3911] zq sending False!
# [3931] mt sending False!
# [4021] kx sending False!
# [7814] zd sending False!
# [7822] zq sending False!
# [7862] mt sending False!
# [8042] kx sending False!
# [11721] zd sending False!
# [11733] zq sending False!
# [11793] mt sending False!
# [12063] kx sending False!
# [15628] zd sending False!
# [15644] zq sending False!
# [15724] mt sending False!
# [16084] kx sending False!
# [19535] zd sending False!
# [19555] zq sending False!
# [19655] mt sending False!
# [20105] kx sending False!
# [23442] zd sending False!
# [23466] zq sending False!
# [23586] mt sending False!
# [24126] kx sending False!
# [27349] zd sending False!
# [27377] zq sending False!
# [27517] mt sending False!
# [28147] kx sending False!
# [31256] zd sending False!

# >>> zd = [3907, 7814, 11721, 15628]
# >>> zd[1]-zd[0]
# 3907
# >>> zd[2]-zd[1]
# 3907
# >>> zdcyc=zd[1]-zd[0]
# >>> zq = [3911, 7822, 11733]
# >>> zq[1]-zq[0],zq[2]-zq[1]
# (3911, 3911)
# >>> zqcyc = zq[1]-zq[0]
# >>> mt = [3931, 7862, 11793]
# >>> mt[1]-mt[0],mt[2]-mt[1]
# (3931, 3931)
# >>> mtcyc=3931
# >>> kx = [4021, 8042, 12063]
# >>> kx[1]-kx[0],kx[2]-kx[1]
# (4021, 4021)
# >>> kxcyc = 4021
# >>> zdcyc*mtcyc*kxcyc*zqcyc
# 241528477694627

#241528477694627