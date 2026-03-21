import numpy as np
import cv2
import time

FRAME_TIME = 10


cap = cv2.VideoCapture(0) #defines the camera to use

last_cap_time = 0

while True:
     ret, frame = cap.read()
     frame_64 = cv2.resize(frame, (512, 512))
     cv2.imshow('frame',frame_64)

     if cv2.waitKey(1) & 0xFF == ord('q'):
         break

cap.release()
cv2.destroyAllWindows()



