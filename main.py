from collections import defaultdict
import math
import numpy as np
import pygame as pg
from pygame.constants import K_SPACE, K_c
from threading import Thread
from time import sleep

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
BOARD_DIM = 25
SQUARE_SIZE = SCREEN_SIZE / BOARD_DIM
BOARD = np.arange(BOARD_DIM ** 2).reshape(BOARD_DIM, BOARD_DIM)


def main():
    launch()


def launch():
    carryOn = True
    clock = pg.time.Clock()
    pg.display.set_caption("AAAAASS")
    path_list = []
    wall_list = []
    while carryOn:

        start = (0, 0)
        goal = (BOARD_DIM - 1, BOARD_DIM - 1)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                carryOn = False

            elif pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                column = int(pos[0] // SQUARE_SIZE)
                row = int(pos[1] // SQUARE_SIZE)
                wall_list.append((row, column))

            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                column = int(pos[0] // SQUARE_SIZE)
                row = int(pos[1] // SQUARE_SIZE)
                try:
                    wall_list.remove((row, column))
                except ValueError:
                    pass

            elif event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    path_list = a_star(wall_list, start, goal)
                    if path_list == "failure":
                        print(path_list)
                        path_list = []
                        wall_list = []
                        continue
                elif event.key == K_c:
                    wall_list = []
                    continue

        grid_constructor(wall_list, path_list, start, goal)

        pg.display.flip()
        clock.tick(120)

    pg.quit()


def grid_constructor(wall_list, path_list, start, goal):
    if BOARD_DIM % 2 == 0:
        box_color(BOARD_DIM, wall_list, path_list, start, goal)
    else:
        box_color(BOARD_DIM + 1, wall_list, path_list, start, goal)


def box_color(second_range, wall_list, path_list, start, goal):
    cnt = 0
    for i in range(BOARD_DIM + 1):
        for j in range(second_range):
            if (i, j) in wall_list:
                color = BLACK
            elif (i, j) == start:
                color = RED
            elif (i, j) == goal:
                color = GREEN
            elif (i, j) in path_list:
                color = BLUE
            elif cnt % 2 == 0:
                color = DARK_GREY
            else:
                color = LIGHT_GREY
            pg.draw.rect(
                SCREEN,
                color,
                [
                    SQUARE_SIZE * j,
                    SQUARE_SIZE * i,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                ],
            )
            cnt += 1
        cnt -= 1


# --------------------------------------------------------------------------- #
#                                    LOGIC                                    #
# --------------------------------------------------------------------------- #


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path


def h(x, goal):
    height = abs(goal[0] - x[0])
    length = abs(goal[1] - x[1])
    return math.sqrt(height ** 2 + length ** 2)


def neighbor_finder(wall_list, current):

    neighbor_coord = set()
    for i in range(-1, 2):
        neighbor_coord.add((current[0] + i, current[1] - 1))
        neighbor_coord.add((current[0] + i, current[1]))
        neighbor_coord.add((current[0] + i, current[1] + 1))
    neighbor_coord.remove(current)

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
        if i not in wall_list:
            neighbor_coord.add(i)

    return neighbor_coord


def a_star(wall_list, start, goal):
    current = ()
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
        neighbors = neighbor_finder(wall_list, current)

        for neighbor in neighbors:
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