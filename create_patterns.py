import numpy as np
import random

import config

WHITE_CONSTANT = config.WHITE_CONSTANT
BLACK_CONSTANT = config.BLACK_CONSTANT

GRID_SIZE = config.GRID_SIZE
BLOCK_SIZE = config.BLOCK_SIZE
RATIO = 2
patterns = []

for i in range(0, GRID_SIZE, BLOCK_SIZE):
    for j in range(0, GRID_SIZE, BLOCK_SIZE):
        pattern = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        # light one block and around it
        pattern[max(0, i -  RATIO * BLOCK_SIZE):(i + RATIO * BLOCK_SIZE), max(0, j - RATIO * BLOCK_SIZE):(j + RATIO * BLOCK_SIZE)] = WHITE_CONSTANT
        #pattern = np.full((GRID_SIZE, GRID_SIZE), WHITE_CONSTANT, dtype=np.uint8)
        patterns.append(pattern)


















