import config
import numpy as np
import cv2
import pyautogui

import create_patterns

SHOW_TIME = config.FRAME_TIME_MILLISEC

#patterns = np.array(create_patterns.patterns)
patterns = np.array(create_patterns.patterns)
num_patterns = len(patterns)
greyscale_patterns = np.astype(patterns * 255, np.uint8)

last_show_time = 0

# Set background to full black screen
screen_width, screen_height = pyautogui.size()
canvas = np.zeros((screen_height, screen_width), np.uint8)
cv2.namedWindow("Full Screen Patterns", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Full Screen Patterns", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Show patterns
for i, pattern in enumerate(greyscale_patterns):
    pattern_height, pattern_width = np.shape(pattern)
    canvas[screen_height - pattern_height:, screen_width - pattern_width:] = pattern
    cv2.imshow("Full Screen Patterns", canvas)

    key = cv2.waitKey(SHOW_TIME) & 0xFF

    if key == ord('q'): # q closes all
        cv2.destroyAllWindows()
        break

    elif key == 13:  # Enter skips to next pattern
        continue

cv2.destroyAllWindows()





