import film_results

frames = film_results.frames_array

import numpy as np

# נניח frames_array: shape (num_frames, height, width)
max_positions = []

for i, frame in enumerate(frames):
    # find the index of the maximum pixel in the flattened frame
    idx = np.argmax(frame)

    # convert the flat index to 2D coordinates (row, col)
    row, col = np.unravel_index(idx, frame.shape)

    max_positions.append((row, col))

print(max_positions)
print(frames)
print(len(frames))
print(len(frames[0]))
print(len(frames[0][0]))