import numpy as np
import random

import config

WHITE_CONSTANT = config.WHITE_CONSTANT
BLACK_CONSTANT = config.BLACK_CONSTANT

GRID_SIZE = config.GRID_SIZE
BLOCK_SIZE = config.BLOCK_SIZE
i_RATIO = config.i_RATIO
j_RATIO = config.j_RATIO
patterns = []
pattern = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
patterns.append(pattern)
for i in range(0, GRID_SIZE, BLOCK_SIZE):
    for j in range(0, GRID_SIZE, BLOCK_SIZE):
        pattern = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        # light one block and around it
        pattern[max(0, i -  i_RATIO * BLOCK_SIZE):(i + i_RATIO * BLOCK_SIZE), max(0, j - j_RATIO * BLOCK_SIZE):(j + j_RATIO * BLOCK_SIZE)] = WHITE_CONSTANT
        patterns.append(pattern)


















