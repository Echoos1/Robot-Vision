#!/usr/bin python generate_aruco.py
"""detect_aruco.py: Detects aruco tags to be used by robot vision and OpenCV for 3D locating information.
"""

__version__ = "1.3.0"

__author__ = "Matthew DiMaggio"
__date__ = "14 June 2023"

import numpy as np
import cv2 as cv
from cv2 import aruco
import glob



# Load Camera Calibration Data
with np.load('CameraCalibCharuco.npz') as X:
    mtx, dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]


# Build projection criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objp = np.zeros((4,3), np.float32)
objp[:,:2] = np.mgrid[0:2,0:2].T.reshape(-1,2)

axis = np.float32([[1,0,0], [0,1,0], [0,0,-1]]).reshape(-1,3)

# Builds video capturing
vid = cv.VideoCapture(0)

def drawOnFrame(frame, corners, ids):
    ids = ids.flatten()

    for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4, 2))
        
        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(markerCorner, 1, mtx, dist)

        cv.drawFrameAxes(frame, mtx, dist, rvecs, tvecs, 1)

        (topLeft, topRight, bottomRight, bottomLeft) = corners2

        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))


        cv.line(frame, topLeft, topRight, (200, 200, 200), 3)
        cv.line(frame, topRight, bottomRight, (200, 200, 200), 3)
        cv.line(frame, bottomRight, bottomLeft, (0, 0, 255), 3)
        cv.line(frame, bottomLeft, topLeft, (0, 255, 0), 3)

        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        cv.drawMarker(frame, (bottomLeft[0], bottomLeft[1]), 3, markerType=cv.MARKER_CROSS)

        cv.putText(frame, str(markerID), (cX-5, cY+5), cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 0, 255), 2)

while (True):

    ret, frame = vid.read()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
    parameters =  aruco.DetectorParameters()
    detector = aruco.ArucoDetector(aruco_dict, parameters)
    corners, ids, rejectedImgPoints = detector.detectMarkers(gray)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)

    if len(corners) > 0:
        drawOnFrame(frame, corners, ids)
            
        cv.imshow("Frame", frame)
        key = cv.waitKey(1) & 0xFF

    else:
        cv.imshow('Frame', frame)
    
vid.release()
# Destroy all the windows
cv.destroyAllWindows()