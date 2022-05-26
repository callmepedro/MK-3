import cv2
import numpy as np


padding = 10
bc_active = (0, 255, 0)
bc_inactive = (0, 0, 255)
thickness = 2

cur_bc = np.array([bc_active, bc_inactive, bc_inactive])


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = np.array(frame)

    wd3 = frame.shape[1] // 3

    cv2.rectangle(frame, (padding, padding), (wd3 - padding, frame.shape[0]-padding), cur_bc.tolist()[0], thickness)
    cv2.rectangle(frame, (wd3 + padding, padding), (2 * wd3 - padding, frame.shape[0]-padding), cur_bc.tolist()[1], thickness)
    cv2.rectangle(frame, (2 * wd3 + padding, padding), (3 * wd3 - padding, frame.shape[0]-padding), cur_bc.tolist()[2], thickness)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_light = np.array([0, 40, 40])
    red_dark = np.array([20, 255, 255])
    mask = cv2.inRange(hsv, red_light, red_dark)

    frame_after = cv2.bitwise_and(frame, frame, mask=mask)
    cv2.imshow('frame', frame)

    pressed_key = cv2.waitKey(1)
    if pressed_key == ord(' '):
        cur_bc = np.roll(cur_bc, 1, axis=0)
    if pressed_key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()