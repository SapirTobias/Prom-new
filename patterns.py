import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import PIL
from numpy.f2py.auxfuncs import throw_error

grid_width = 4
grid_height = 4

grid = np.arange(grid_width * grid_height, dtype = int)
binary_grid = np.array([format(x, 'b') for x in grid], dtype=int).reshape(grid_height, grid_width)

print(binary_grid)

# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
num_patterns = np.log2(grid_height * grid_width)
if int(num_patterns) != num_patterns:
    throw_error("grid size must ensure the number of patterns is an integer")
patterns = []
num_patterns = int(num_patterns)

for i in range(num_patterns):
    # Get the i th digit of each element in grid = the color of the pixel in this pattern
    pattern = (binary_grid >> i) & 1
    patterns.append(pattern)

patterns = np.array(patterns)
print(patterns)

#













