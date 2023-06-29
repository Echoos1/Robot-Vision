#!/usr/bin python generate_aruco.py
"""calibrate_camera_chess.py: Uses a chessboard grid to calibrate the camera to improve 3D accuracy.
"""

__version__ = "0.1.0"

__author__ = "Matthew DiMaggio"
__date__ = "15 June 2023"

import numpy as np
import cv2 as cv
from cv2 import aruco
import glob

cbw = 6
cbh = 9

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
objp = np.zeros((cbw*cbh,3), np.float32)
objp[:,:2] = np.mgrid[0:cbh,0:cbw].T.reshape(-1,2)

# Arrays to store object points and image points from all the images
objpoints = [] #3D points in real world space
imgpoints = [] #2D points in image plane

images = glob.glob('calib_img/chessboard/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find the chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (cbh,cbw), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, (cbh,cbw), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(150)

cv.destroyAllWindows()

# Calibrate Camera from images
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# Save Camera Calibration Data
np.savez('CameraCalib.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)