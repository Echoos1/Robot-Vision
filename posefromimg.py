#!/usr/bin python generate_aruco.py
"""detect_aruco.py: Locates the camera pose in space.
"""

__version__ = "0.1.0"

__author__ = "Matthew DiMaggio"
__date__ = "10 July 2023"
__requires__ = "opencv_contrib_python==4.5.5.62"

import math

import numpy as np
import cv2 as cv
from cv2 import aruco


def rotMtxToQuat(rotm):
    tr = rotm[0][0] + rotm[1][1] + rotm[2][2]

    if tr > 0:
        S = math.sqrt(tr + 1.0) * 2
        qw = 0.25 * S
        qx = (rotm[2][1] - rotm[1][2]) / S
        qy = (rotm[0][2] - rotm[2][0]) / S
        qz = (rotm[1][0] - rotm[0][1]) / S
    elif (rotm[0][0] > rotm[1][1]) and (rotm[0][0] > rotm[2][2]):
        S = math.sqrt(1.0 + rotm[0][0] - rotm[1][1] - rotm[2][2]) * 2
        qw = (rotm[2][1] - rotm[1][2]) / S
        qx = 0.25 * S
        qy = (rotm[0][1] + rotm[1][0]) / S
        qz = (rotm[0][2] + rotm[2][0]) / S
    elif rotm[1][1] > rotm[2][2]:
        S = math.sqrt(1.0 + rotm[1][1] - rotm[0][0] - rotm[2][2]) * 2
        qw = (rotm[0][2] - rotm[2][0]) / S
        qx = (rotm[0][1] + rotm[1][0]) / S
        qy = 0.25 * S
        qz = (rotm[1][2] + rotm[2][1]) / S
    else:
        S = math.sqrt(1.0 + rotm[2][2] - rotm[0][0] - rotm[1][1]) * 2
        qw = (rotm[1][0] - rotm[0][1]) / S
        qx = (rotm[0][2] + rotm[2][0]) / S
        qy = (rotm[1][2] + rotm[2][1]) / S
        qz = 0.25 * S

    return [qw, qx, qy, qz]


def analyzeImage(image):
    # Load Camera Calibration Data
    with np.load("CameraCalibArUCo.npz") as X:
        mtx, dist, calib_rvec, calib_tvec = [
            X[i] for i in ("mtx", "dist", "rvecs", "tvecs")
        ]

    # Specify ArUCo Dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

    # Define ArUCo Boards
    pickupboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 0)
    dropoffboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 30)

    # Open image to read
    frame = cv.imread(image)

    # Detect ArUCo markers
    gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejects = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    corners, ids, _, _ = aruco.refineDetectedMarkers(
        gray, dropoffboard, corners, ids, rejects, mtx, dist
    )

    if len(corners) > 0:  # If any markers are detected...
        # Uses position of ArUCo tags with matching IDs to find board coordinates
        ret_p, rvec_p, tvec_p = cv.aruco.estimatePoseBoard(
            corners, ids, pickupboard, mtx, dist, calib_rvec, calib_tvec
        )
        ret_d, rvec_d, tvec_d = cv.aruco.estimatePoseBoard(
            corners, ids, dropoffboard, mtx, dist, calib_rvec, calib_tvec
        )

        if ret_p > 0:  # If the "Pickup" ArUCo board is detected...
            pz = ((tvec_p[2][0])) / 1.69
            px = -((-0.37 * pz) - (tvec_p[0][0]))
            py = -((-0.34 * pz) - (tvec_p[1][0]))
            pquatx = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[0]
            pquaty = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[1]
            pquatz = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[2]
            pquatw = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[3]
        else:
            pz = 0
            px = 0
            py = 0
            pquatx = 0
            pquaty = 0
            pquatz = 0
            pquatw = 0

        if ret_d > 0:  # If the "Dropoff" ArUCo board is detected...
            dz = ((tvec_d[2][0])) / 1.69
            dx = -((-0.37 * dz) - (tvec_d[0][0]))
            dy = -((-0.34 * dz) - (tvec_d[1][0]))
            dquatx = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[0]
            dquaty = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[1]
            dquatz = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[2]
            dquatw = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[3]
        else:
            dz = 0
            dx = 0
            dy = 0
            dquatx = 0
            dquaty = 0
            dquatz = 0
            dquatw = 0

        return [
            [px, py, pz, pquatx, pquaty, pquatz, pquatw],
            [dx, dy, dz, dquatx, dquaty, dquatz, dquatw],
        ]

    else:  # If no ArUCo markers are detected...
        return [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]


def main():
    pose = analyzeImage("testing.jpg")
    print("Pickup Pose")
    print(f"X={pose[0][0]:.01f} Y={pose[0][1]:.01f} Z={pose[0][2]:.01f}")
    print(f"qX={pose[0][3]:.01f} qY={pose[0][4]:.01f} ", end="")
    print(f"qZ={pose[0][5]:.01f} qW={pose[0][6]:.01f}")
    print("Dropoff Pose")
    print(f"X={pose[1][0]:.01f} Y={pose[1][1]:.01f} Z={pose[1][2]:.01f}")
    print(f"qX={pose[1][3]:.04f} qY={pose[1][4]:.04f} ", end="")
    print(f"qZ={pose[1][5]:.04f} qW={pose[1][6]:.04f}")


if __name__ == "__main__":
    main()
