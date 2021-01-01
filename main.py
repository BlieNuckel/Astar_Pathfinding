from collections import defaultdict
import math
import numpy as np

BOARD_DIM = 10
BOARD = np.arange(BOARD_DIM ** 2).reshape(BOARD_DIM, BOARD_DIM)


def main():
    print(BOARD)
    print(a_star(0, 99))


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
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
        if (
            i[0] != -1
            and i[1] != -1
            and i[0] != BOARD_DIM
            and i[1] != BOARD_DIM
        ):
            new_neighbor_coord.add(i)

    return new_neighbor_coord


def a_star(start, goal):
    current = None
    openSet = set()
    openSet.add(start)
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start, goal)

    while len(openSet) != 0:

        for i in openSet:
            temp_current = math.inf
            if current is None:
                current = start
                break
            if fScore[i] < fScore[temp_current]:
                temp_current = i
                current = i

        if current == goal:
            return reconstruct_path(cameFrom, current)

        openSet.discard(current)
        neighbors = neighbor_finder(current)

        for neighbor_coord in neighbors:
            neighbor = BOARD[neighbor_coord[0]][neighbor_coord[1]]
            tentative_gScore = gScore[current] + h(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    return print("failure")


if __name__ == "__main__":
    main()