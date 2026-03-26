import numpy as np
import config

GRID_SIZE = config.GRID_SIZE
NUM_PATTERNS = config.NUM_FRAMES

# Create grid with the unique binary code for each cell
grid = np.arange(GRID_SIZE * GRID_SIZE, dtype = int)
binary_grid = np.array([format(x, 'b') for x in grid], dtype=int).reshape(GRID_SIZE, GRID_SIZE)

patterns = []
NUM_PATTERNS = int(NUM_PATTERNS)

for i in range(NUM_PATTERNS):
    # Get the i th digit of each element in grid, which represents whether the pixel is on in this pattern
    pattern = (binary_grid >> i) & 1
    patterns.append(pattern)















