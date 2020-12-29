from collections import defaultdict
import math
from typing import DefaultDict


def reconstruct_path(cameFrom, current):
    total_path = current
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.prepend(current)
    return total_path


def a_star(start, goal, h):
    openSet = {start}
    cameFrom = {}
    gscore = defaultdict(lambda: math.inf)
    gscore[start] = 0

    fscore = defaultdict(lambda: math.inf)
    fscore[start] = h(start)
    
    while len(openSet) is not 0:
        current = 
