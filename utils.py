import itertools

from constants import *


def neighbours(x, y):
    for nx, ny in itertools.product(
        range(
            max(x-1, 0), min(x+2, GRID_WIDTH)
        ),
        range(
            max(y-1, 0), min(y+2, GRID_HEIGHT))):
        yield nx, ny


def cursor2world(x, y):
    return x // CELL_WIDTH, y // CELL_HEIGHT
