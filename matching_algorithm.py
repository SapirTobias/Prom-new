import cv2
import numpy as np

import config
import camera_settings as camera_settings
import create_patterns as create_patterns
from camera_settings import GRID_SIZE

BLACK_CONSTANT = 0
WHITE_CONSTANT = 255
GREY_CONSTANT = 123

FRAME_COUNT = config.NUM_FRAMES

patterns = create_patterns.patterns
frames = camera_settings.frames

#This function returns the weighted average between all of the frames in the current index
def weighted_avg(index):

    pattern_i_j = [pattern[index[0], index[1]] for pattern in patterns] #list with all of the patterns in the index place
    frames_i_j = [f[index[0], index[1]] for f in frames] #list with all of the patterns in the index place
    if np.sum(pattern_i_j) == 0:
        val = GREY_CONSTANT
    else:
        val =  np.dot(frames_i_j, pattern_i_j) / np.sum(pattern_i_j)
    print(val)
    return val

threshold = GREY_CONSTANT
match_mat = np.full((GRID_SIZE, GRID_SIZE, 2), -1, dtype=int)

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):

        exit_l_loop = False

        for l in range(GRID_SIZE):

            if exit_l_loop:
                break

            for m in range(GRID_SIZE):
                wrong_match = False # We don't yet know that this match is wrong

                for pattern, frame in zip(patterns, frames):
                    # if the pixel [l,m] in the frame isn't as we expected, then this isn't the match ->
                    # move to next iteration on m, by breaking the most inner loop
                    if (frame[l,m] < threshold and pattern[i,j] == 1) or (frame[l,m] >= threshold and pattern[i,j] == 0):
                        wrong_match = True # It isn't a correct match
                        break

                if not wrong_match:
                    # If we got here, [l,m] is [i,j]'s match, as they matched for all frames
                    match_mat[i,j] = [l, m]
                    exit_l_loop = True # ensure l loop is exited
                    break # exit the m loop


dual_image = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):

        # If no match found, take a grey value, else average the frames at the matched value
        if match_mat[i,j, 0] == -1:
            dual_image[i,j] = GREY_CONSTANT
        else:
            dual_image[i,j] = int(weighted_avg(match_mat[i,j]))

print(dual_image)
cv2.imshow("dual_image", dual_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
