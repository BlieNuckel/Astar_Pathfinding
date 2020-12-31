from collections import defaultdict
import math
import numpy as np

BOARD_DIM = 10
BOARD = np.arange(BOARD_DIM ** 2).reshape(10, 10)


def main():
    print(BOARD)
    neighbor_finder(10)


def reconstruct_path(cameFrom, current):
    total_path = current
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.prepend(current)
    return total_path


def h(x, goal):
    x_coord = (np.where(BOARD == x)[0][0], np.where(BOARD == x)[1][0])
    goal_coord = (np.where(BOARD == goal)[0][0], np.where(BOARD == goal)[1][0])
    height = abs(x_coord[0] - goal_coord[0])
    length = abs(x_coord[1] - goal_coord[1])
    return math.sqrt(height ** 2 + length ** 2)


def neighbor_finder(current):
    current_coord = (
        np.where(BOARD == current)[0][0],
        np.where(BOARD == current)[1][0],
    )

    print(current_coord)

    neighbor_coord = set()
    other_neighbor_coord = set()
    for i in range(-1, 2):
        other_neighbor_coord.add((current_coord[0] + i, current_coord[1] - 1))
        other_neighbor_coord.add((current_coord[0] + i, current_coord[1]))
        other_neighbor_coord.add((current_coord[0] + i, current_coord[1] + 1))


def a_star(start, goal):
    current = None
    openSet = {start}
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start, goal)

    while len(openSet) != 0:
        for node in openSet:
            if current is None or fScore[current] > fScore[node]:
                current = node

        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.remove(current)
        neighbors = neighbor_finder(current)

        for neighbor in neighbors:
            if neighbor < 0 or neighbor > 99:
                neighbors.remove(neighbor)
            tentative_gScore = gScore[current] + h(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    return "failure"


if __name__ == "__main__":
    main()