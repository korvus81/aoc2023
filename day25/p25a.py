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
import networkx as nx
from util import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open("input.txt","r") as f:
    input = f.readlines()

example = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr""".splitlines()

## to test against example
#input = example

def parse(l):
    pre,post = l.split(":")
    name = pre.strip()
    post = post.strip().split()
    return (name,post)

lines = [parse(s.strip()) for s in input]
#pp(lines)

connections = {}
for n,cmps in lines:
    if n not in connections:
        connections[n] = set()
    connections[n].update(cmps)
    for cmp in cmps:
        if cmp not in connections:
            connections[cmp] = set()
        connections[cmp].add(n)


#ic(connections)
G = nx.Graph()
for k in connections.keys():
    G.add_node(k)
    for cmp in connections[k]:
        G.add_edge(k,cmp)

ic(nx.clustering(G))
ic(nx.maximal_independent_set(G))
ic(nx.minimum_edge_cut(G))
# ('vkd', 'qfb'), ('xzz', 'kgl'), ('hqq', 'xxq')
#ic(nx.approximation.max_clique(G))

G2 = G.copy()
G2.remove_edge('vkd', 'qfb')
G2.remove_edge('xzz', 'kgl')
G2.remove_edge('hqq', 'xxq')



def find_nodes_connected_to(GRAPH, start_node):
    connected = set()
    connected.add(start_node)
    nodes_to_check = [start_node]
    while len(nodes_to_check) > 0:
        for n2 in GRAPH.neighbors(nodes_to_check[0]):
            if n2 not in connected:
                nodes_to_check.append(n2)
            connected.add(n2)
        nodes_to_check.pop(0)
    return connected

nodes_connected_to_vkd = find_nodes_connected_to(G2,"vkd")
nodes_connected_to_qfb = find_nodes_connected_to(G2,"qfb")
ic(nodes_connected_to_vkd)
ic(nodes_connected_to_qfb)

ic(len(nodes_connected_to_vkd))
ic(len(nodes_connected_to_qfb))
ic(len(nodes_connected_to_vkd) * len(nodes_connected_to_qfb))

exit()

with open("graph.dot","w") as fout:
    fout.write("graph {\n")
    written = set()
    for k,v in connections.items():
        for cmp in v:
            c1,c2 = sorted([k,cmp])
            if (c1,c2) not in written:
                written.add((c1,c2))
                fout.write(f"  {c1} -- {c2} [label=\"{c1}-{c2}\"]\n")
    fout.write("}\n")

def collapse(conns):
    tightly_connected = set()
    for k,cmps in conns.items():
        for cmp1,cmp2 in combinations(cmps,2):
            if cmp1 not in conns:
                ic(cmp1,conns)
            if cmp2 in conns[cmp1]:
                group = tuple(sorted([k,cmp1,cmp2]))
                tightly_connected.add(group)
    #ic(tightly_connected)
    tightly_connected_nodes = dict()
    for nodes in tightly_connected:
        for n in nodes:
            tightly_connected_nodes[n] = nodes
    #ic(tightly_connected_nodes)
    collapsed_connections = {}
    for n,cmps in lines:
        if n in tightly_connected_nodes:
            n = "-".join(tightly_connected_nodes[n])
        if n not in collapsed_connections:
            collapsed_connections[n] = set()
        new_cmps = set()
        for cmp in cmps:
            if cmp in tightly_connected_nodes:
                cmp = "-".join(tightly_connected_nodes[cmp])
            if cmp != n:
                new_cmps.add(cmp)
        collapsed_connections[n].update(new_cmps)
        for cmp in cmps:
            if cmp in tightly_connected_nodes:
                cmp = "-".join(tightly_connected_nodes[cmp])
            if cmp not in collapsed_connections:
                collapsed_connections[cmp] = set()
            collapsed_connections[cmp].add(n)
    return collapsed_connections

collapsed_connections = collapse(connections)
while len(collapsed_connections) > 100:
    ic(len(collapsed_connections))
    collapsed_connections = collapse(collapsed_connections)



with open("graph-collapsed.dot","w") as fout:
    fout.write("graph {\n")
    written = set()
    for k,v in connections.items():
        for cmp in v:
            c1,c2 = sorted([k,cmp])
            if (c1,c2) not in written:
                written.add((c1,c2))
                fout.write(f"  {c1} -- {c2} [label=\"{c1}-{c2}\"]\n")
    fout.write("}\n")
ic(collapsed_connections)