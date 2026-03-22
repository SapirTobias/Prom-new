import time

import camera_settings
import create_patterns
import numpy as np
import cv2
SHOW_TIME = camera_settings.FRAME_TIME

patterns = np.array(create_patterns.patterns)
num_patterns = len(patterns)
greyscale_patterns = np.astype(patterns * 255, np.uint8)

count = 0
last_show_time = 0
for i, pattern in enumerate(greyscale_patterns):
     current_time = time.time()
     # If SHOW_TIME seconds passed, show the next pattern
     if int(current_time - last_show_time) > SHOW_TIME:
         last_cap_time = current_time
         print(pattern)
         cv2.imshow(f"Pattern {i}", pattern)

     # If pressed q
     if cv2.waitKey(1) & 0xFF == ord('q'):
         break





