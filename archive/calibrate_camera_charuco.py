#!/usr/bin python generate_aruco.py
"""calibrate_camera_charuco.py: Uses a chessboard grid to calibrate the camera to improve 3D accuracy.
"""

__version__ = "0.2.0"

__author__ = "Matthew DiMaggio"
__date__ = "15 June 2023"

import numpy as np
import cv2 as cv
from cv2 import aruco
import glob

# ChAruco board variables
charuco_row = 7
charuco_col = 5 
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)

charuco_brd = aruco.CharucoBoard(
        size=(charuco_col,charuco_row),
        squareLength=0.03,
        markerLength=0.015,
        dictionary=aruco_dict)


# Create the arrays and variables we'll use to store info like corners and IDs from images processed
corners_all = [] # Corners discovered in all images processed
ids_all = [] # Aruco ids corresponding to corners discovered
image_size = None # Determined at runtime

images = glob.glob('calib_img/charuco/*.jpg')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find aruco markers in the query image
    corners, ids, _ = aruco.detectMarkers(
            image=gray,
            dictionary=aruco_dict)
    
    if len(corners) > 0:

        # Outline the aruco markers found in our query image
        img = aruco.drawDetectedMarkers(
                image=img, 
                corners=corners)

        response, charuco_corners, charuco_ids = aruco.interpolateCornersCharuco(
                markerCorners=corners,
                markerIds=ids,
                image=gray,
                board=charuco_brd)
    else:
        response = 0
    
    # If a Charuco board was found, let's collect image/corner points
    # Requiring at least 20 squares
    if response > 20:
        # Add these corners and ids to our calibration arrays
        corners_all.append(charuco_corners)
        ids_all.append(charuco_ids)
        
        # Draw the Charuco board we've detected to show our calibrator the board was properly detected
        img = aruco.drawDetectedCornersCharuco(
                image=img,
                charucoCorners=charuco_corners,
                charucoIds=charuco_ids)
       
        # If our image size is unknown, set it now
        if not image_size:
            image_size = gray.shape[::-1]
    
        # Reproportion the image, maxing width or height at 1000
        proportion = max(img.shape) / 1000.0
        img = cv.resize(img, (int(img.shape[1]/proportion), int(img.shape[0]/proportion)))
        # Pause to display each image, waiting for key press
        cv.imshow('Charuco board', img)
        cv.waitKey(0)
    else:
        print("Not able to detect a charuco board in image: {}".format(fname))
        cv.imshow('Charuco board', img)
        cv.waitKey(0)


# Destroy any open CV windows
cv.destroyAllWindows()

# Make sure at least one image was found
if len(images) < 1:
    # Calibration failed because there were no images, warn the user
    print("Calibration was unsuccessful. No images of charucoboards were found. Add images of charucoboards and use or alter the naming conventions used in this file.")
    # Exit for failure
    exit()

# Make sure we were able to calibrate on at least one charucoboard by checking
# if we ever determined the image size
if not image_size:
    # Calibration failed because we didn't see any charucoboards of the PatternSize used
    print("Calibration was unsuccessful. We couldn't detect charucoboards in any of the images supplied. Try changing the patternSize passed into Charucoboard_create(), or try different pictures of charucoboards.")
    # Exit for failure
    exit()

# Now that we've seen all of our images, perform the camera calibration
# based on the set of points we've discovered
ret, mtx, dist, rvecs, tvecs = aruco.calibrateCameraCharuco(
        charucoCorners=corners_all,
        charucoIds=ids_all,
        board=charuco_brd,
        imageSize=image_size,
        cameraMatrix=None,
        distCoeffs=None)

# Save Camera Calibration Data
np.savez('CameraCalibCharuco.npz', ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)