# import the necessary packages
import argparse
import time
from collections import deque

import cv2
import imutils
import numpy as np
from imutils.video import VideoStream



# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=32,
                help="max buffer size")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])
# allow the camera or video file to warm up
time.sleep(2.0)


def nothing(x):
    pass


cv2.namedWindow('marking')

cv2.createTrackbar('H Lower', 'marking', 0, 255, nothing)
cv2.createTrackbar('H Higher', 'marking', 255, 255, nothing)
cv2.createTrackbar('S Lower', 'marking', 0, 255, nothing)
cv2.createTrackbar('S Higher', 'marking', 255, 255, nothing)
cv2.createTrackbar('V Lower', 'marking', 0, 255, nothing)
cv2.createTrackbar('V Higher', 'marking', 255, 255, nothing)

while (1):
    _, img = camera.read()
    img = cv2.flip(img, 1)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hL = cv2.getTrackbarPos('H Lower', 'marking')
    hH = cv2.getTrackbarPos('H Higher', 'marking')
    sL = cv2.getTrackbarPos('S Lower', 'marking')
    sH = cv2.getTrackbarPos('S Higher', 'marking')
    vL = cv2.getTrackbarPos('V Lower', 'marking')
    vH = cv2.getTrackbarPos('V Higher', 'marking')

    LowerRegion = np.array([hL, sL, vL], np.uint8)
    upperRegion = np.array([hH, sH, vH], np.uint8)

    redObject = cv2.inRange(hsv, LowerRegion, upperRegion)

    kernal = np.ones((1, 1), "uint8")

    red = cv2.morphologyEx(redObject, cv2.MORPH_OPEN, kernal)
    red = cv2.dilate(red, kernal, iterations=1)

    res1 = cv2.bitwise_and(img, img, mask=red)

    cv2.imshow("Masking ", res1)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        camera.release()
        cv2.destroyAllWindows()
        break
