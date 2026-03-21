import numpy as np
from numpy.f2py.auxfuncs import throw_error

GRID_SIZE = 512
GRID_WIDTH = GRID_SIZE
GRID_HEIGHT = GRID_SIZE

grid = np.arange(GRID_WIDTH * GRID_HEIGHT, dtype = int)
binary_grid = np.array([format(x, 'b') for x in grid], dtype=int).reshape(GRID_HEIGHT, GRID_WIDTH)

# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
num_patterns = np.log2(GRID_HEIGHT * GRID_WIDTH)
if int(num_patterns) != num_patterns:
    throw_error("grid size must ensure the number of patterns is an integer")
patterns = []
num_patterns = int(num_patterns)

for i in range(num_patterns):
    # Get the i th digit of each element in grid = is the pixel on in this pattern
    pattern = (binary_grid >> i) & 1
    patterns.append(pattern)















