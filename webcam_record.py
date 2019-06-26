
import numpy as np
import cv2

Cap = cv2.VideoCapture(0)
writerC = cv2.VideoWriter('/home/joev/Videos/Color_Video.mp4', cv2.VideoWriter_fourcc(*'XVID'),8, (640, 480))

while True: 
    ret, frameC = Cap.read()     
    frameC = cv2.resize(frameC,(640, 480))
    writerC.write(frameC)
    cv2.imshow('frameC', frameC)
    frame = None
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
