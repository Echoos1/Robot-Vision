#!/usr/bin python generate_aruco.py
"""Vision_Test.py: Tests the vision code for use in RaspiVision.
Detects the position and orientation of ArUCo Tag Boards and 
displays their axis frames on the screen. Recommended for use on a 
PC or other test device with a monitor prior to loading code on camera.
"""

__version__ = "0.7.1"

__author__ = "Matthew DiMaggio"
__date__ = "14 June 2023"
__requires__ = 'opencv_contrib_python==4.5.5.62'

import math
import numpy as np
import cv2 as cv
from cv2 import aruco
import pkg_resources
pkg_resources.require('opencv_contrib_python==4.5.5.62')




def drawOnFrame(frame, corners, ids):
    ids = ids.flatten()

    for (markerCorner, markerID) in zip(corners, ids):
        corners = markerCorner.reshape((4, 2))
        (topLeft, topRight, bottomRight, bottomLeft) = corners

        topRight = (int(topRight[0]), int(topRight[1]))
        bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
        bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
        topLeft = (int(topLeft[0]), int(topLeft[1]))

        cv.line(frame, topLeft, topRight, (0, 255, 0), 2)
        cv.line(frame, topRight, bottomRight, (0, 255, 0), 2)
        cv.line(frame, bottomRight, bottomLeft, (0, 255, 0), 2)
        cv.line(frame, bottomLeft, topLeft, (0, 255, 0), 2)

        cX = int((topLeft[0] + bottomRight[0]) / 2.0)
        cY = int((topLeft[1] + bottomRight[1]) / 2.0)

        cv.drawMarker(frame, 
                      (bottomLeft[0], 
                       bottomLeft[1]), 
                      3, 
                      markerType=cv.MARKER_CROSS)

        cv.putText(frame, 
                   str(markerID), 
                   (cX-5, cY+5), 
                   cv.FONT_HERSHEY_DUPLEX, 
                   0.5, 
                   (255, 0, 255), 
                   2)


def rotMtxToQuat(rotm):
    tr = rotm[0][0] + rotm[1][1] + rotm[2][2]

    if (tr > 0):
        S = math.sqrt(tr+1.0) * 2
        qw = 0.25 * S
        qx = (rotm[2][1] - rotm[1][2]) / S
        qy = (rotm[0][2] - rotm[2][0]) / S 
        qz = (rotm[1][0] - rotm[0][1]) / S 
    elif ((rotm[0][0] > rotm[1][1]) and (rotm[0][0] > rotm[2][2])):
        S = math.sqrt(1.0 + rotm[0][0] - rotm[1][1] - rotm[2][2]) * 2
        qw = (rotm[2][1] - rotm[1][2]) / S
        qx = 0.25 * S
        qy = (rotm[0][1] + rotm[1][0]) / S 
        qz = (rotm[0][2] + rotm[2][0]) / S 
    elif (rotm[1][1] > rotm[2][2]):
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

    return [qw,qx,qy,qz]


def drawCustomAxis(frame, axisCenter, axisSize, rvec, tvec, mtx, dist):  # Draws a custom axis on a specified object point

    # Object Coordinates to draw Axis
    axisPoints = np.float32([
                    [axisCenter[0], axisCenter[1], axisCenter[2]],
                    [axisCenter[0]+axisSize, axisCenter[1], axisCenter[2]],
                    [axisCenter[0], axisCenter[1]+axisSize, axisCenter[2]],
                    [axisCenter[0], axisCenter[1], axisCenter[2]+axisSize],
                ]).reshape((-1, 1, 3))
    
    # Convert Object points to Pixel Coordinates
    imagePoints, _ = cv.projectPoints(axisPoints, rvec, tvec, mtx, dist)
    imagePoints = imagePoints.astype(int)

    # Draw Axis on the video frame
    cv.line(frame, imagePoints[0,0], imagePoints[1,0], (0,0,255), 3)
    cv.line(frame, imagePoints[0,0], imagePoints[2,0], (0,255,0), 3)
    cv.line(frame, imagePoints[0,0], imagePoints[3,0], (255,0,0), 3)

    return frame


def streamPoseToFile(file, rvec, tvec):  # Writes position data to a file

    """
    In file.txt:
    
    X
    Y
    Z
    QuatW
    QuatX
    QuatY
    QuatZ
    """

    quat = rotMtxToQuat(cv.Rodrigues(rvec)[0])  # Converts Rodrigues Angles to Rotation Matrix, then to Quaternion
    try:  # Attempt to write to the file
        with open(file, "w") as txt:
            txt.writelines([f'{str(tvec[0][0])}\n',
                            f'{str(tvec[1][0])}\n',
                            f'{str(tvec[2][0])}\n',
                            f'{str(quat[0])}\n',
                            f'{str(quat[1])}\n',
                            f'{str(quat[2])}\n',
                            f'{str(quat[3])}\n'])
    except PermissionError:  # As file is live read, this prevents errors when trying to write to an open file
        pass


def findFocalLength(frame, axisCenter, axisSize, rvec, tvec, mtx, dist):

    # Object Coordinates to draw Axis
    axisPoints = np.float32([
                    [axisCenter[0], axisCenter[1], axisCenter[2]],
                    [axisCenter[0]+axisSize, axisCenter[1], axisCenter[2]]
                ]).reshape((-1, 1, 3))
    
    # Convert Object points to Pixel Coordinates
    imagePoints, _ = cv.projectPoints(axisPoints, rvec, tvec, mtx, dist)
    imagePoints2 = imagePoints.astype(int)

    # Draw Axis on the video frame
    cv.line(frame, imagePoints2[0,0], imagePoints2[1,0], (0,0,255), 3)

    x1 = imagePoints[0,0][0]
    y1 = imagePoints[0,0][1]
    x2 = imagePoints[1,0][0]
    y2 = imagePoints[1,0][1]

    pixDistance = math.sqrt(((x2-x1)**2) + ((y2 - y1)**2))
    
    print(pixDistance)

    focal_length = (pixDistance * 285.75) / axisSize
    print(focal_length)

    cv.imshow("Frame", frame)
    cv.waitKey(0)
    quit()    


def refineDistance(axisCenter, axisSize, rvec, tvec, mtx, dist):
    focal_length = 640.7080633483813

    axisPoints = np.float32([
                    [axisCenter[0], axisCenter[1], axisCenter[2]],
                    [axisCenter[0]+axisSize, axisCenter[1], axisCenter[2]]
                ]).reshape((-1, 1, 3))
    
    # Convert Object points to Pixel Coordinates
    imagePoints, _ = cv.projectPoints(axisPoints, rvec, tvec, mtx, dist)

    x1 = imagePoints[0,0][0]
    y1 = imagePoints[0,0][1]
    x2 = imagePoints[1,0][0]
    y2 = imagePoints[1,0][1]

    pixDistance = math.sqrt(((x2-x1)**2) + ((y2 - y1)**2))

    trueDistance = (axisSize * focal_length) / pixDistance

    return trueDistance


def refineX(frame, axisCenter, axisSize, rvec, tvec, mtx, dist):
    camera_center = (frame.shape[:2][1]/2,frame.shape[:2][0]/2)

    axisPoints = np.float32([
                    [axisCenter[0], axisCenter[1], axisCenter[2]],
                    [axisCenter[0]+axisSize, axisCenter[1], axisCenter[2]],
                    [axisCenter[0], axisCenter[1]+axisSize, axisCenter[2]]
                ]).reshape((-1, 1, 3))
    
    # Convert Object points to Pixel Coordinates
    imagePoints, _ = cv.projectPoints(axisPoints, rvec, tvec, mtx, dist)

    x1 = imagePoints[0,0][0]
    y1 = imagePoints[0,0][1]
    x2 = imagePoints[1,0][0]
    y2 = imagePoints[1,0][1]

    x1c = imagePoints[0,0][0]-camera_center[0]
    y1c = imagePoints[0,0][1]-camera_center[1]

    pixDistance = math.sqrt(((x2-x1)**2) + ((y2 - y1)**2))

    mmPerPix = axisSize/pixDistance
    
    X = x1c*mmPerPix
    Y = y1c*mmPerPix

    return X,Y


def main():
    # Load Camera Calibration Data
    with np.load('CameraCalibArUCo.npz') as X:
        mtx, dist, calib_rvec, calib_tvec = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    # Builds video capturing
    vid = cv.VideoCapture(0)

    # Specify ArUCo Dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

    # Define ArUCo Boards
    pickupboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 0)
    dropoffboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 30)

    while (True):

        # Capture a video frame for analysis
        ret, frame = vid.read()

        # Kill Video analsis when user presses "Q" key
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

        # Detect ArUCo markers
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        parameters =  aruco.DetectorParameters_create()
        corners, ids, rejects = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        corners, ids, _, _ = aruco.refineDetectedMarkers(gray, dropoffboard, corners, ids, rejects, mtx, dist)
        frame_markers = aruco.drawDetectedMarkers(frame, corners)

        if len(corners) > 0:  # If any markers are detected...

            # Uses position of ArUCo tags with matching IDs to find board coordinates
            ret_p, rvec_p, tvec_p = cv.aruco.estimatePoseBoard(corners, ids, pickupboard, mtx, dist, calib_rvec, calib_tvec)
            ret_d, rvec_d, tvec_d = cv.aruco.estimatePoseBoard(corners, ids, dropoffboard, mtx, dist, calib_rvec, calib_tvec)
            
            if ret_p > 0:  # If the "Pickup" ArUCo board is detected...

                pz = ((tvec_p[2][0]))/1.69
                px = -((-0.37*pz)-(tvec_p[0][0]))
                py = -((-0.34*pz)-(tvec_p[1][0]))
                
                cv.drawFrameAxes(frame, mtx, dist, rvec_p, tvec_p, 70)  # Draws True Origin
                drawCustomAxis(frame, [95, 115, 0], 70, rvec_p, tvec_p, mtx, dist)  # Draws Center Axis

            if ret_d> 0:  # If the "Dropoff" ArUCo board is detected...
                
                dz = ((tvec_d[2][0]))/1.69
                dx = -((-0.37*dz)-(tvec_d[0][0]))
                dy = -((-0.34*dz)-(tvec_d[1][0]))

                # Writes the position and rotation to a file to be read live by a 3D simulator for debug purposes
                file_d = "C:/Users/mdimaggio/Documents/Summer Research/2023/datastream.txt"
                streamPoseToFile(file_d, rvec_d, [[dx],[dy],[dz]])
                
                cv.drawFrameAxes(frame, mtx, dist, rvec_d, tvec_d, 70)  # Draws True Origin
                drawCustomAxis(frame, [95, 115, 0], 70, rvec_d, tvec_d, mtx, dist)  # Draws Center Axis

            # Show the video frame with added elements
            cv.imshow("Frame", frame)

        else:  # If no ArUCo markers are detected...
            # Show the video
            cv.imshow('Frame', frame)

    vid.release()  # Stop capturing videos and release the camera to the system 
    cv.destroyAllWindows()  # Destroy all the windows


if __name__ == "__main__":
    main()
