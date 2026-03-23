import numpy as np
import random

import config

WHITE_CONSTANT = config.WHITE_CONSTANT
BLACK_CONSTANT = config.BLACK_CONSTANT

GRID_SIZE = config.GRID_SIZE
BLOCK_SIZE = config.BLOCK_SIZE
patterns = []

for i in range(0, GRID_SIZE, BLOCK_SIZE):
    for j in range(0, GRID_SIZE, BLOCK_SIZE):
        pattern = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)
        # light one block
        if j % 5 == 0:
            pattern[i:i + BLOCK_SIZE, j:j + BLOCK_SIZE] = WHITE_CONSTANT
        else:
            pattern[i:i + BLOCK_SIZE, j:j + BLOCK_SIZE] = BLACK_CONSTANT
        patterns.append(pattern)


















