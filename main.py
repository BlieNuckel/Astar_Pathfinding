from collections import defaultdict
import math
import numpy as np

BOARD_DIM = 10
BOARD = np.arange(BOARD_DIM ** 2).reshape(10, 10)


def main():
    a_star(10, 15)


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

    neighbor_coord = set()
    for i in range(-1, 2):
        neighbor_coord.add((current_coord[0] + i, current_coord[1] - 1))
        neighbor_coord.add((current_coord[0] + i, current_coord[1]))
        neighbor_coord.add((current_coord[0] + i, current_coord[1] + 1))
    neighbor_coord.remove(current_coord)

    new_neighbor_coord = set()
    for i in neighbor_coord:
        if i[0] != -1 and i[1] != -1 and i[0] != 10 and i[1] != 10:
            new_neighbor_coord.add(i)

    return new_neighbor_coord


def a_star(start, goal):
    current = None
    openSet = set()
    openSet.add(start)
    print(openSet)
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start, goal)

    while len(openSet) != 0:
        for node in openSet:
            print("line 63", node)
            if current is None or fScore[current] > fScore[node]:
                print("line 66")
                current = node

        if current == goal:
            print("line 68")
            return reconstruct_path(cameFrom, current)

        openSet.discard(current)
        neighbors = neighbor_finder(current)

        for neighbor in neighbors:
            print("line 75")
            tentative_gScore = gScore[current] + h(
                current, BOARD[neighbor[0]][neighbor[1]]
            )
            print(tentative_gScore)
            print(gScore[neighbor])
            if tentative_gScore < gScore[neighbor]:
                print("line 80")
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(
                    BOARD[neighbor[0]][neighbor[1]], goal
                )
                if neighbor not in openSet:
                    print("line 87")
                    openSet.add(neighbor)

    return print("failure")


if __name__ == "__main__":
    main()