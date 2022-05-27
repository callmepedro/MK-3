import cv2
import numpy as np


width = 640
height = 480

detect_frame_width = 80
detect_frame_height = 80
pixel_skip_factor = 2


def gstreamer_pipeline(
        capture_width=width,
        capture_height=height,
        display_width=width,
        display_height=height,
        framerate=30,
        flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=true"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )


top_y = (height - detect_frame_height) // 2
bottom_y = (height + detect_frame_height) // 2
top_x1 = (width // 3 - detect_frame_width) // 2
top_x2 = top_x1 + width // 3
top_x3 = top_x2 + width // 3

# top_left  top_right  bottom_left  bottom_right
borders = [[top_x1, top_x1 + detect_frame_width, top_y, bottom_y],
           [top_x2, top_x2 + detect_frame_width, top_y, bottom_y],
           [top_x3, top_x3 + detect_frame_width, top_y, bottom_y]]


def cnt_colors(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    colors_cnt = [0] * 7
    for i in range(borders[0][2] + 1, borders[0][3], pixel_skip_factor):
        for j in range(borders[0][0] + 1, borders[0][1] + 1, pixel_skip_factor):
            if hsv[i][j][1] < 50 or hsv[i][j][2] < 50:
                continue
            if 0 <= hsv[i][j][0] <= 14 or 170 <= hsv[i][j][0] <= 179:
                colors_cnt[0] += 1
            if 15 <= hsv[i][j][0] <= 20:
                colors_cnt[1] += 1
            if 21 <= hsv[i][j][0] <= 35:
                colors_cnt[2] += 1
            if 36 <= hsv[i][j][0] <= 79:
                colors_cnt[3] += 1
            if 80 <= hsv[i][j][0] <= 100:
                colors_cnt[4] += 1
            if 101 <= hsv[i][j][0] <= 133:
                colors_cnt[5] += 1
            if 134 <= hsv[i][j][0] <= 169:
                colors_cnt[6] += 1

    return colors_cnt


def get_color(frame):
    pixels_count = detect_frame_width * detect_frame_height // pixel_skip_factor**2

    all_colors_cnt = cnt_colors(frame)

    if max(all_colors_cnt) / pixels_count <= 0.18:
        return ""

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


# cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=4), cv2.CAP_GSTREAMER)
cap = cv2.VideoCapture(0)

text_on = ""
cnt = 0
while True:
    cnt += 1

    ret, frame = cap.read()
    frame = np.asarray(frame)

    if cnt % 10 == 0:
        text_on = get_color(frame)
        cnt = 0

    cv2.rectangle(frame, (borders[0][0], borders[0][2]), (borders[0][1], borders[0][3]), (0, 255, 0), 2)
    cv2.rectangle(frame, (borders[1][0], borders[1][2]), (borders[1][1], borders[1][3]), (0, 0, 255), 2)
    cv2.rectangle(frame, (borders[2][0], borders[2][2]), (borders[2][1], borders[2][3]), (0, 0, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,
                text_on,
                (50, 50),
                font, 1,
                (255, 255, 255),
                2,
                cv2.LINE_4)

    cv2.imshow('frame', frame)

    pressed_key = cv2.waitKey(1)
    if pressed_key == ord(' '):
        borders = np.roll(borders, -1, axis=0)
    if pressed_key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
