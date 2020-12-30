from collections import defaultdict
import math
import heapq
from numpy.core.records import array


def board_constructor():
    board = array([[]])


def reconstruct_path(cameFrom, current):
    total_path = current
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.prepend(current)
    return total_path


def h(x, goal):
    return math.sqrt(x ** 2 + goal)


def d(current, neighbor):
    
    

def a_star(start, goal):
    current = None
    openSet = [start]
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start)

    while len(openSet) is not 0:
        for node in openSet:
            if current is None or fScore[current] > fScore[node]:
                current = node

        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.heappop(current)
        for neighbor in current:
            tentative_gScore = gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.heappush(neighbor)

    return "failure"