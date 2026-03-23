import numpy as np
import config

GRID_SIZE = config.GRID_SIZE
BLOCK_SIZE = config.BLOCK_SIZE
patterns = []

for i in range(0, GRID_SIZE, BLOCK_SIZE):
    for j in range(0, GRID_SIZE, BLOCK_SIZE):
        pattern = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)  # black background

        # light one block
        pattern[i:i + BLOCK_SIZE, j:j + BLOCK_SIZE] = 1

        patterns.append(pattern)


















