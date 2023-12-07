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
from util import *

with open("input.txt","r") as f:
    input = f.readlines()

example = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""".splitlines()

## to test against example
#input = example

lines = [s.strip().split() for s in input]
pp(lines)

cardtypes = "AKQJT98765432"
# smaller is better, assuming we sort in order
cardstrength = {c:pos for pos,c in enumerate(cardtypes)}
ic(cardstrength)

def typeval(cards):
    #cards = sorted(list(hand),key=lambda c:cardstrength[c])
    #ic(cards)
    count_of_cards = {c:0 for c in cardtypes}
    for c in cards:
        count_of_cards[c] += 1
    
    if all([c == cards[0] for c in cards]):
        # 5 of a kind
        return 0
    elif max(count_of_cards.values()) == 4:#all([c == cards[0] for c in cards[0:4]]) or all([c == cards[0] for c in cards[1:5]]):
        # 4 of a kind
        return 1
    elif len(set(cards)) == 2:
        # two types of cards, if not 4 of a kind, must be full house
        return 2
    elif max(count_of_cards.values()) == 3: #len(set(cards)) == 3:
        # three of a kind
        return 3
    elif max(count_of_cards.values()) == 2:
        if len(set(cards)) == 3:
            # two pair if we have at most two of a kind and three kinds of cards
            return 4
        else:
            # one pair            
            return 5
    else: # high card
        return 6

hands_and_bids = []
for hand,num in lines:
    bid = int(num)
    cards = sorted(list(hand),key=lambda c:cardstrength[c])
    typval = typeval(cards)
    cardvals = tuple(cardstrength[c] for c in hand) # this should be in original order!
    hand_rank = (typval,cardvals)
    #ic(hand,hand_rank,bid)
    hands_and_bids.append((hand_rank,bid))
#ic(hands_and_bids)
hands_and_bids = sorted(hands_and_bids,reverse=True)
ic(hands_and_bids)
totalscore = 0
for i,(hand,bid) in enumerate(hands_and_bids):
    rank = i + 1
    score = rank * bid
    #ic(rank,hand,bid)
    #ic(score)
    totalscore += score
ic(totalscore)
# right 255048101
