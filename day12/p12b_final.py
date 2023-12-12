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
import pprint

preferredWidth = 220
pptr = pprint.PrettyPrinter(width=preferredWidth)
ic.configureOutput(argToStringFunction=pptr.pformat)
ic.lineWrapWidth = preferredWidth

import re
from itertools import combinations,permutations
from multiprocessing import Pool
# https://docs.python.org/3/library/multiprocessing.html#multiprocessing.pool.Pool.map
# with Pool(processes_count) as p:
#   p.map(<function>, <input>)

from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1""".splitlines()

example2 = """?#?#?#?#?#?#?#? 1,3,1,6""".splitlines()
example3 = """?###???????? 3,2,1""".splitlines()

## to test against example
#input = example

lines = [s.strip().split() for s in input]
lines = [[s,[int(n) for n in nums.split(",")]] for s,nums in lines]
pp(lines)

def getpermutations(line):
    perms = []
    for i,ch in enumerate(line):
        if ch == "?":
            p1 = getpermutations(line[:i]+"."+line[i+1:])
            p2 = getpermutations(line[:i]+"#"+line[i+1:])
            return p1 + p2
    return [line]


@lru_cache(maxsize=1024*1024)
def count_matches(line,runs):
    # see if we have a match starting at line[0]
    count = 0
    current_match = False
    charsneeded = sum(runs) + len(runs) - 1
    if len(line) < charsneeded or len(runs) == 0:
        return 0
    currun = runs[0]
    try:
        if all(ch == "?" or ch == "#" for ch in line[:currun]) and \
            (len(line)==currun or line[currun] == "." or line[currun] == "?"):
            # possible match!  Check the rest
            #print(f"Possible match at '{line}' run of {currun} ")
            if len(runs) == 1:
                if all(ch == "." or ch == "?" for ch in line[currun+1:]):
                    #print(f"Last run ({runs}) line ({line}) matches, returning 1")
                    count += 1 # match done! COULD BE OTHER MATCHES SO CONTINUE
                else:
                    pass
                    #print(f"Last run ({runs}) line ({line}) DOES NOT MATCH, returning 0")
                    #return 0 # other crud at the end
            else:
                #print(f"Checking if '{line[currun+1:]}' matches {runs[1:]}...")
                mtchs = count_matches(line[currun+1:],runs[1:])
                #ic(count,mtchs, line[currun+1:],runs[1:])
                count += mtchs
    except IndexError:
        pass

    # this is because if we are on a #, we can't match starting on the next character
    if line[0] != "#":
        count += count_matches(line[1:],runs)
    #ic(line,runs,count)
    return count

ic(count_matches('??????#??',(4,1)))
ic(count_matches('???????#??',(4,1)))
ic(count_matches('.???????#??',(4,1)))

cnt = count_matches('???????#???.???????#???.???????#??', (4, 1, 4, 1, 4, 1, 4, 1))
ic(cnt, 140)
print()
cnt = count_matches('.???????#???.???????#???.???????#???.???????#???.???????#??',(4, 1, 4, 1, 4, 1, 4, 1, 4, 1))
ic(cnt, 316756)

if True:
    print("\n\n=====\n\n")
    assert 1 == count_matches('???.###', (1,1,3))
    assert 4 == count_matches('.??..??...?##.', (1,1,3))
    assert 1 == count_matches('?#?#?#?#?#?#?#?', (1,3,1,6))

    assert 150 == count_matches('###??????????###????????', (3, 2, 1, 3, 2, 1))
    assert 150 == count_matches('?????????###????????', (2, 1, 3, 2, 1))
    assert 0 == count_matches('###????????', (2, 1))
    assert 10 == count_matches('????###????????', (3, 2, 1))

    assert 1 == count_matches('???.###????.###????.###????.###????.###', (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3))
    assert 16384 == count_matches('.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.?.??..??...?##.', (1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3, 1, 1, 3))
    assert 1 == count_matches('?#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#???#?#?#?#?#?#?#?', (1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6, 1, 3, 1, 6))
    assert 16 == count_matches('????.#...#...?????.#...#...?????.#...#...?????.#...#...?????.#...#...', (4, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 1, 4, 1, 1))
    assert 2500 == count_matches('????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.?????.######..#####.', (1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5, 1, 6, 5))
    assert 506250 == count_matches('?###??????????###??????????###??????????###??????????###????????', (3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1, 3, 2, 1))
    assert 316756 == count_matches('.???????#???.???????#???.???????#???.???????#???.???????#??',(4, 1, 4, 1, 4, 1, 4, 1, 4, 1))
    print("\n\n=====\n\n")
# count = count_matches('###????????', (2, 1))
# ic(count)
# print("=====")
# count = count_matches('????###????????', (3, 2, 1))
# ic(count)
# time.sleep(10)
counts = 0
for linenum,(l,runs) in enumerate(lines):
    # runs = runs of damaged springs
    
    
    # prefix with ? then remove the first
    l = (("?"+l)*5)[1:]
    runs = runs * 5

    ic(linenum,l,runs)

    count = count_matches(l,tuple(runs))
    ic(count)
    counts += count
    ic(counts)
    
ic(counts)
# 8458924659133 is too low :( )
# 8475948826693 was right