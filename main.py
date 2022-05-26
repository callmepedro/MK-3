import cv2
import numpy as np


width = 640
height = 480
wd3 = width // 3
padding = 10
bc_active = (0, 255, 0)
bc_inactive = (0, 0, 255)
thickness = 2

red_light = np.array([0, 60, 60])
red_dark = np.array([14, 255, 255])
orange_light = np.array([15, 60, 60])
orange_dark = np.array([20, 255, 255])
yellow_light = np.array([20, 60, 60])
yellow_dark = np.array([35, 255, 255])
green_light = np.array([36, 60, 60])
green_dark = np.array([74, 255, 255])
blue_light = np.array([75, 60, 60])
blue_dark = np.array([100, 255, 255])
darkblue_light = np.array([101, 60, 60])
darkblue_dark = np.array([133, 255, 255])
purple_light = np.array([134, 60, 60])
purple_dark = np.array([169, 255, 255])
red2_light = np.array([170, 60, 60])
red2_dark = np.array([179, 255, 255])

border_colors = np.array([bc_active, bc_inactive, bc_inactive])

borders = [[padding, wd3 - padding, padding, height - padding],
           [wd3 + padding, 2 * wd3 - padding, padding, height - padding],
           [2 * wd3 + padding, 3 * wd3 - padding, padding, height - padding]]


def cnt_pixels(frame, cur_mask):
    frame_after = cv2.bitwise_and(frame, frame, mask=cur_mask)
    p_cnt = 0
    for i in range(borders[0][2] + 1, borders[0][3]):
        for j in range(borders[0][0] + 1, borders[0][1] + 1):
            if frame_after[i][j][1] != 0:
                p_cnt += 1
    return p_cnt


def get_color(frame):
    pixels_count = (borders[0][3] - borders[0][2]) * (borders[0][1] - borders[0][0])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    red_mask = cv2.inRange(hsv, red_light, red_dark)
    orange_mask = cv2.inRange(hsv, orange_light, orange_dark)
    yellow_mask = cv2.inRange(hsv, yellow_light, yellow_dark)
    green_mask = cv2.inRange(hsv, green_light, green_dark)
    blue_mask = cv2.inRange(hsv, blue_light, blue_dark)
    darkblue_mask = cv2.inRange(hsv, darkblue_light, darkblue_dark)
    purple_mask = cv2.inRange(hsv, purple_light, purple_dark)
    red2_mask = cv2.inRange(hsv, red2_light, red2_dark)

    all_colors_cnt = [0] * 7
    all_colors_cnt[0] += cnt_pixels(frame, red_mask)
    all_colors_cnt[1] += cnt_pixels(frame, orange_mask)
    all_colors_cnt[2] += cnt_pixels(frame, yellow_mask)
    all_colors_cnt[3] += cnt_pixels(frame, green_mask)
    all_colors_cnt[4] += cnt_pixels(frame, blue_mask)
    all_colors_cnt[5] += cnt_pixels(frame, darkblue_mask)
    all_colors_cnt[6] += cnt_pixels(frame, purple_mask)
    all_colors_cnt[0] += cnt_pixels(frame, red2_mask)

    if max(all_colors_cnt) / pixels_count <= 0.15:
        return "nothing"

    color_idx = all_colors_cnt.index(max(all_colors_cnt))
    if color_idx == 0:
        return "red"
    if color_idx == 1:
        return "orange"
    if color_idx == 2:
        return "yellow"
    if color_idx == 3:
        return "green"
    if color_idx == 4:
        return "blue"
    if color_idx == 5:
        return "darkblue"
    if color_idx == 6:
        return "purple"


cap = cv2.VideoCapture(0)

cnt = 0
while True:
    ret, frame = cap.read()
    frame = np.array(frame)

    cv2.rectangle(frame, (padding, padding), (wd3 - padding, frame.shape[0]-padding), border_colors.tolist()[0], thickness)
    cv2.rectangle(frame, (wd3 + padding, padding), (2 * wd3 - padding, frame.shape[0]-padding), border_colors.tolist()[1], thickness)
    cv2.rectangle(frame, (2 * wd3 + padding, padding), (3 * wd3 - padding, frame.shape[0]-padding), border_colors.tolist()[2], thickness)

    if cnt % 25 == 0:
        print(get_color(frame))

    cv2.imshow('frame', frame)

    cnt += 1
    pressed_key = cv2.waitKey(1)
    if pressed_key == ord(' '):
        border_colors = np.roll(border_colors, 1, axis=0)
        borders = np.roll(borders, -1, axis=0)
    if pressed_key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()