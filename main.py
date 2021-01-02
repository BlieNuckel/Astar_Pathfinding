from collections import defaultdict
import math
import sys
import numpy as np
import pygame as pg
from pygame.constants import K_1, K_2, K_3, K_SPACE, K_c

pg.init()

BLACK = (0, 0, 0, 255)
DARK_GREY = (46, 46, 46)
LIGHT_GREY = (87, 87, 87)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (65, 125, 230)

BRUSH_SIZE = 1
SCREEN_SIZE = 700
SCREEN = pg.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
BOARD_DIM = 50
MARGIN = 250 / BOARD_DIM
SQUARE_SIZE = (SCREEN_SIZE + MARGIN) / BOARD_DIM
BOARD = np.arange(BOARD_DIM ** 2).reshape(BOARD_DIM, BOARD_DIM)

START = (0, 0)
GOAL = (BOARD_DIM - 1, BOARD_DIM - 1)


def main():
    launch()


def launch():
    BRUSH_SIZE = 1
    carryOn = True
    clock = pg.time.Clock()
    pg.display.set_caption("AAAAASS")
    path_list = []
    wall_list = []

    grid_constructor()
    while carryOn:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                carryOn = False

            elif pg.mouse.get_pressed()[0]:
                pos = pg.mouse.get_pos()
                column = int(pos[0] // SQUARE_SIZE)
                row = int(pos[1] // SQUARE_SIZE)
                if BRUSH_SIZE == 1:
                    if (row, column) != START and (row, column) != GOAL:
                        wall_list.append((row, column))
                else:
                    brush_function(wall_list, (row, column), BRUSH_SIZE, False)
                wall_drawer(wall_list)

            elif pg.mouse.get_pressed()[2]:
                pos = pg.mouse.get_pos()
                column = int(pos[0] // SQUARE_SIZE)
                row = int(pos[1] // SQUARE_SIZE)
                if BRUSH_SIZE == 1:
                    if (row, column) in wall_list:
                        wall_list.remove((row, column))
                        specific_box_color((row, column), WHITE)
                else:
                    brush_function(wall_list, (row, column), BRUSH_SIZE, True)
                wall_drawer(wall_list)

            elif event.type == pg.KEYDOWN:
                if event.key == K_SPACE:
                    path_list = a_star(wall_list)
                    wall_list = []
                    grid_constructor()
                    for i in path_list:
                        specific_box_color(i, BLUE)
                    if path_list == "failure":
                        print(path_list)
                        path_list = []
                        wall_list = []
                        continue
                elif event.key == K_c:
                    wall_list = []
                    grid_constructor()
                    continue
                elif event.key == K_1:
                    BRUSH_SIZE = 1
                elif event.key == K_2:
                    BRUSH_SIZE = 3
                elif event.key == K_3:
                    BRUSH_SIZE = 5

        pg.display.flip()
        clock.tick()

    pg.quit()


def grid_constructor():
    for i in range(BOARD_DIM):
        for j in range(BOARD_DIM):
            if (i, j) == START:
                color = GREEN
            elif (i, j) == GOAL:
                color = RED
            else:
                color = WHITE

            pg.draw.rect(
                SCREEN,
                color,
                [
                    SQUARE_SIZE * j,
                    SQUARE_SIZE * i,
                    SQUARE_SIZE - MARGIN,
                    SQUARE_SIZE - MARGIN,
                ],
            )


def wall_drawer(wall_list):
    for coord in wall_list:
        specific_box_color((coord[0], coord[1]), BLACK)


def specific_box_color(coord, color):
    pg.draw.rect(
        SCREEN,
        color,
        [
            SQUARE_SIZE * coord[1],
            SQUARE_SIZE * coord[0],
            SQUARE_SIZE - MARGIN,
            SQUARE_SIZE - MARGIN,
        ],
    )


def brush_function(wall_list, current, size, delete):
    if not delete:
        for i in range(-(size // 2), (size // 2) + 1):
            for j in range(-(size // 2), (size // 2) + 1):
                if (current[0] + i, current[1] + j) != START and (
                    current[0] + i,
                    current[1] + j,
                ) != GOAL:
                    wall_list.append((current[0] + i, current[1] + j))
    else:
        for i in range(-(size // 2), (size // 2) + 1):
            for j in range(-(size // 2), (size // 2) + 1):
                if (current[0] + i, current[1] + j) in wall_list:
                    if (current[0] + i, current[1] + j) != START and (
                        current[0] + i,
                        current[1] + j,
                    ) != GOAL:
                        wall_list.remove((current[0] + i, current[1] + j))
                        specific_box_color(
                            (current[0] + i, current[1] + j), WHITE
                        )


# --------------------------------------------------------------------------- #
#                                    LOGIC                                    #
# --------------------------------------------------------------------------- #


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.insert(0, current)
    return total_path


def h(x, y):
    height = abs(y[0] - x[0])
    length = abs(y[1] - x[1])
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
            specific_box_color(i, GREEN)
            pg.display.flip()
            pg.time.Clock().tick()

    return neighbor_coord


def event_handler():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()


def a_star(wall_list):
    current = ()
    openSet = set()
    openSet.add(START)
    cameFrom = {}
    gScore = defaultdict(lambda: math.inf)
    gScore[START] = 0

    fScore = defaultdict(lambda: math.inf)
    fScore[START] = h(START, GOAL)

    while len(openSet) != 0:
        event_handler()
        temp_current = -1
        for i in openSet:
            if current is None:
                current = START
                break
            if fScore[i] < fScore[temp_current]:
                temp_current = i
                current = i

        if current == GOAL:
            return reconstruct_path(cameFrom, current)

        openSet.discard(current)
        grid_constructor()
        wall_drawer(wall_list)
        for i in openSet:
            specific_box_color(i, LIGHT_BLUE)
        neighbors = neighbor_finder(wall_list, current)
        pg.display.flip()
        pg.time.Clock().tick()

        for neighbor in neighbors:
            tentative_gScore = gScore[current] + h(current, neighbor)
            if tentative_gScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + h(neighbor, GOAL)
                if neighbor not in openSet:
                    openSet.add(neighbor)

    return "failure"


if __name__ == "__main__":
    main()