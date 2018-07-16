import cv2
import numpy as np


def detect(img):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Define range of blue color in HSV
    lower_blue = np.array([110, 50, 50])
    upper_blue = np.array([130, 255, 255])
    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-And mask and original image
    res = cv2.bitwise_and(img, img, mask=mask)

    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    m = cv2.moments(mask)
    if m["m00"] != 0:
        cx = int(m["m10"]/m["m00"])
        cy = int(m["m01"]/m["m00"])

    else:
        cx = 0
        cy = 0
    print(cx, cy)
    return cx, cy


cam = cv2.VideoCapture(0)
# Resize
cam.set(3, 640)
cam.set(4, 480)
# latest point
lx, ly = (0, 0)

while True:
    # Take each frame
    _, frame = cam.read()
    cv2.imshow('origin', frame)

    x, y = detect(frame)
    cv2.line(frame, (x, y), (lx, ly), (0, 0, 200), 5)
    lx, ly = x, y

    cv2.imshow('tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()