from collections import defaultdict
import math
import numpy as np
import pygame as pg

pg.init()

BLACK = (0, 0, 0)
DARK_GREY = (46, 46, 46)
LIGHT_GREY = (87, 87, 87)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_SIZE = 700
SIZE = (SCREEN_SIZE, SCREEN_SIZE)
SCREEN = pg.display.set_mode(SIZE)
BOARD_DIM = 10
SQUARE_SIZE = SCREEN_SIZE / BOARD_DIM
BOARD = np.arange(BOARD_DIM ** 2).reshape(BOARD_DIM, BOARD_DIM)
WALL_SET = {1, 2, 3, 6, 7, 8, 12, 13, 18}


def main():
    print(BOARD)
    print(a_star(0, 4))
    launch()


def launch():
    carryOn = True
    clock = pg.time.Clock()
    pg.display.set_caption("AAAAASS")

    while carryOn:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                carryOn = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                column = int((pos[0] // SQUARE_SIZE) - 1)
                row = int((pos[1] // SQUARE_SIZE) - 1)
                BOARD[row][column] = -1

        grid_constructor()

        pg.display.flip()
        clock.tick(120)

    pg.quit()


def grid_constructor():
    if BOARD_DIM % 2 == 0:
        box_color(BOARD_DIM)
    else:
        box_color(BOARD_DIM + 1)


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path


def h(x, goal):
    x_coord = (np.where(BOARD == x)[0][0], np.where(BOARD == x)[1][0])
    goal_coord = (np.where(BOARD == goal)[0][0], np.where(BOARD == goal)[1][0])
    height = abs(goal_coord[0] - x_coord[0])
    length = abs(goal_coord[1] - x_coord[1])
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

    neighbor_coord = set()
    for i in new_neighbor_coord:
        if BOARD[i[0]][i[1]] != -1:
            neighbor_coord.add(i)

    return neighbor_coord


def a_star(start, goal):
    np.where(BOARD == start) = -2
    np.where(BOARD == goal) = -3
    current = None
    openSet = set()
    openSet.add(start)
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[start] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[start] = h(start, goal)

    while len(openSet) != 0:
        temp_current = -1
        for i in openSet:
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

    return "failure"


def wall_adder(num_set):
    for i in num_set:
        coord = (np.where(BOARD == i)[0][0], np.where(BOARD == i)[1][0])
        BOARD[coord[0]][coord[1]] = -1


def box_color(second_range):
    cnt = 0
    for i in range(BOARD_DIM + 1):
        for j in range(second_range):
            if BOARD[i - 1][j - 1] == -1:
                color = BLACK
                pg.draw.rect(
                    SCREEN,
                    BLACK,
                    [
                        SQUARE_SIZE * j,
                        SQUARE_SIZE * i,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ],
                )
            elif BOARD[i - 1][j - 1] == -2:
                color = RED
            elif BOARD[i - 1][j - 1] == -3:
                color = GREEN   
            elif cnt % 2 == 0:
                color = DARK_GREY
                pg.draw.rect(
                    SCREEN,
                    DARK_GREY,
                    [
                        SQUARE_SIZE * j,
                        SQUARE_SIZE * i,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ],
                )
            else:
                color = LIGHT_GREY
                pg.draw.rect(
                    
                    SCREEN,
                    LIGHT_GREY,
                    [
                        SQUARE_SIZE * j,
                        SQUARE_SIZE * i,
                        SQUARE_SIZE,
                        SQUARE_SIZE,
                    ],
                )
        
            cnt += 1
        cnt -= 1


if __name__ == "__main__":
    main()