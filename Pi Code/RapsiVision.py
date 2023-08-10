#!/usr/bin python RaspiVision.py
"""RaspiVision.py: Locates the camera pose in space.
"""

__version__ = "1.0.0"

__author__ = "Matthew DiMaggio"
__date__ = "10 July 2023"
__requires__ = "opencv_contrib_python==4.5.5.62"

import time
import math
import RPi.GPIO as GPIO

from picamera2 import Picamera2
from pathlib import Path
import numpy as np
import cv2 as cv
from cv2 import aruco


class Settings:    
    initCount = 0




# Camera Configuration and Setup
print("[INFO] Configuring Camera")
time1 = time.time()
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (1920,1080)}, 
    lores={"size": (640,480)}, 
    display="lores"
    )
picam2.configure(camera_config)
with np.load("CameraCalibArUCo.npz") as X:
    mtx, dist, calib_rvec, calib_tvec = [
        X[i] for i in ("mtx", "dist", "rvecs", "tvecs")
    ]
time2=time.time()
print(f'[INFO] Configuration Complete! Took {(time2-time1):.01f} seconds')


def intTobinary(int):
	if  abs(int) > 2047:
		binary = f'{0:012b}'
	else:
		binary = f'{abs(int):012b}'

	binarylst = []
	for i in range(len(binary)):
		binarylst.append(binary[i])

	if int < 0:
		binarylst[0] = 1
	else:
		binarylst[0] = 0

	return binarylst


def StopCallback():
	print("Callback")
	setBin([1,0,1,0,1,0,1,0,1,0,1,0])
	print("Lights On")
	print("Waiting 3")
	time.sleep(3)
	resetPins()
	print("Lights Off")
	print("Cleanup")
	GPIO.cleanup()
	print("Quit")
	quit()


def resetPins():
    GPIO.output(Bi1, 0) # Blue
    GPIO.output(Bi2, 0) # Blue
    GPIO.output(Bi3, 0) # Blue
    GPIO.output(Bi4, 0) # Blue
    GPIO.output(Bi5, 0) # Yellow
    GPIO.output(Bi6, 0) # Yellow
    GPIO.output(Bi7, 0) # Yellow
    GPIO.output(Bi8, 0) # Yellow
    GPIO.output(Bi9, 0) # Green
    GPIO.output(Bi10, 0) # Green
    GPIO.output(Bi11, 0) # Green
    GPIO.output(BiS, 0) # Green
    GPIO.output(CamStep, 0) # Red


def setBin(binary):
	GPIO.output(Bi1, int(binary[-1]))
	GPIO.output(Bi2, int(binary[-2]))
	GPIO.output(Bi3, int(binary[-3]))
	GPIO.output(Bi4, int(binary[-4]))
	GPIO.output(Bi5, int(binary[-5]))
	GPIO.output(Bi6, int(binary[-6]))
	GPIO.output(Bi7, int(binary[-7]))
	GPIO.output(Bi8, int(binary[-8]))
	GPIO.output(Bi9, int(binary[-9]))
	GPIO.output(Bi10, int(binary[-10]))
	GPIO.output(Bi11, int(binary[-11]))
	GPIO.output(BiS, int(binary[-12]))


def step(stepMessage = None):
    if not GPIO.input(robReady):
            main()
    # Sends Step Signal
    GPIO.output(CamStep, 1)
    if stepMessage:
        print(f'[STEP] {stepMessage}')
    # Waits for a full Step Signal from robot, on then off
    while True:
        if GPIO.input(robStep) and GPIO.input(robReady):
            break
        if not GPIO.input(robReady):
            main()
        time.sleep(.05)
    while True:
        if not GPIO.input(robStep) and GPIO.input(robReady):
            break
        if not GPIO.input(robReady):
            main()
        time.sleep(.05)
        
    # Turns off step signal
    GPIO.output(CamStep, 0)
    time.sleep(.05)


def getInput():
    robstep = input("ENTER for CONTINUE, ELSE for QUIT: ")
    if robstep == "":
        return True
    else:
        return False


def rotMtxToQuat(rotm: np.array) -> list:
    """Converts a Rotation Matrix to a 4x1 Quaternion.
    
    Credits:
        Copyright (c) 1998-2023 Martin John Baker
        https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToQuaternion/

    Args:
        rotm (np.array): A 3x3 Roation Matrix returned by opencv functions

    Returns:
        list: A 4x1 WXYZ Quaternion -- [W,X,Y,Z]
    """  
      
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


def takePhoto(filepath: str) -> bool:
    """Takes a photo with a Raspberry Pi Camera

    Args:
        filepath (str): The filepath of the image to be taken

    Returns:
        bool: Returns True if taken successfully, False if not
    """   
    try:
        print("[INFO] Taking Picture...")
        time1=time.time()
        picam2.start()
        picam2.capture_file(filepath)
        picam2.stop()
        time2=time.time()
        print(f'[INFO] Capturing Done! Took {(time2-time1):.01f} seconds')
        print(f'[INFO] Saved at: {filepath}')
        return True
    except Exception:
        print("[ERROR] Capturing Failed")
        return False


def analyzeImage(filepath: str) -> list:
    """Uses OpenCV to find the camera pose using an image of ArUCo Boards.

    Args:
        filepath (str): The filepath of the image to be analysed.

    Returns:
        list: Two nested Lists of each ArUCo board position and rotation
        [[PickupBoard Pose and Rot],[Dropoff Board Pose and Rot]]
    """    
    
    print("[INFO] Analysing Image...")
    time1=time.time()
    
    # Specify ArUCo Dictionary
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

    # Define ArUCo Boards
    pickupboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 0)
    dropoffboard = cv.aruco.GridBoard_create(5, 6, 30, 10, aruco_dict, 30)

    # Open image to read
    frame = cv.imread(str(filepath))

    # Detect ArUCo markers
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejects = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    corners, ids, _, _ = aruco.refineDetectedMarkers(
        gray, dropoffboard, corners, ids, rejects, mtx, dist
    )
    _ = aruco.drawDetectedMarkers(frame, corners)

    if len(corners) > 0:  # If any markers are detected...
        # Uses position of ArUCo tags with matching IDs to find board coordinates
        ret_p, rvec_p, tvec_p = cv.aruco.estimatePoseBoard(
            corners, ids, pickupboard, mtx, dist, calib_rvec, calib_tvec
        )
        ret_d, rvec_d, tvec_d = cv.aruco.estimatePoseBoard(
            corners, ids, dropoffboard, mtx, dist, calib_rvec, calib_tvec
        )
        
        if ret_p > 0:  # If the "Pickup" ArUCo board is detected...
            pz = tvec_p[2][0]
            #pz = tvec_p[2][0] * 1.279
            px = tvec_p[0][0]
            #px = -((.023 * pz) - (tvec_p[0][0]))
            py = tvec_p[1][0]
            #py = -((.018 * pz) - (tvec_p[1][0]))
            pquatx = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[0]
            pquaty = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[1]
            pquatz = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[2]
            pquatw = rotMtxToQuat(cv.Rodrigues(rvec_p)[0])[3]
            
            cv.drawFrameAxes(frame, mtx, dist, rvec_p, tvec_p, 70)  # Draws True Origin
        else:
            pz = 0
            px = 0
            py = 0
            pquatx = 0
            pquaty = 0
            pquatz = 0
            pquatw = 0

        if ret_d > 0:  # If the "Dropoff" ArUCo board is detected...
            dz = tvec_d[2][0] * 1.279
            dx = -((0.169 * dz) - (tvec_d[0][0]))
            dy = -((0.455 * dz) - (tvec_d[1][0]))
            dquatx = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[0]
            dquaty = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[1]
            dquatz = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[2]
            dquatw = rotMtxToQuat(cv.Rodrigues(rvec_d)[0])[3]
            
            cv.drawFrameAxes(frame, mtx, dist, rvec_p, tvec_p, 70)  # Draws True Origin
        else:
            dz = 0
            dx = 0
            dy = 0
            dquatx = 0
            dquaty = 0
            dquatz = 0
            dquatw = 0

        cv.imwrite(str(filepath),frame)
        time2=time.time()
        print(f'Finished Analysis! Took {(time2-time1):.01f} seconds')
        return [
            [px, py, pz, pquatx, pquaty, pquatz, pquatw],
            [dx, dy, dz, dquatx, dquaty, dquatz, dquatw],
        ]

    else:  # If no ArUCo markers are detected...
        time2=time.time()
        print(f'DONE! No Markers Found! Took {(time2-time1):.01f} seconds')
        return [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]


def sendItem(item,itemName = None):
    # Send Item Whole
    if itemName:
        print(f'Sending {itemName} whole...')
    item_whole = (f'{item:.03f}'.split("."))[0]
    item_whole_bin = intTobinary(int(item_whole))
    setBin(item_whole_bin)
    step(stepMessage="Waiting for read confirmation...")
    print("Sent!")
    
    # Send Item Decimal
    if itemName:
        print(f'Sending {itemName} decimal...')
    item_decimal = (f'{item:.03f}'.split("."))[1]
    item_decimal_bin = intTobinary(int(item_decimal))
    setBin(item_decimal_bin)
    step(stepMessage="Waiting for read confirmation...")
    print("Sent!")


def sendToRob(pose):
    # ArUCo Board 0_29 Pickup:
    pX,pY,pZ = pose[0][0],pose[0][1],pose[0][2]
    pQW,pQX,pQY,pQZ = pose[0][3],pose[0][4],pose[0][5],pose[0][6]
    
    # ArUCo Board 30_59 Dropoff:
    dX,dY,dZ = pose[1][0],pose[1][1],pose[1][2]
    dQW,dQX,dQY,dQZ = pose[1][3],pose[1][4],pose[1][5],pose[1][6]
    
    # Send Pickup Boards
    sendItem(pX,itemName="Pickup X")
    sendItem(pY,itemName="Pickup Y")
    sendItem(pZ,itemName="Pickup Z")
    sendItem(pQW*1000,itemName="Pickup QW")
    sendItem(pQX*1000,itemName="Pickup QX")
    sendItem(pQY*1000,itemName="Pickup QY")
    sendItem(pQZ*1000,itemName="Pickup QZ")
    # Send Dropoff Boards
    sendItem(dX,itemName="Dropoff X")
    sendItem(dY,itemName="Dropoff Y")
    sendItem(dZ,itemName="Dropoff Z")
    sendItem(dQW*1000,itemName="Dropoff QW")
    sendItem(dQX*1000,itemName="Dropoff QX")
    sendItem(dQY*1000,itemName="Dropoff QY")
    sendItem(dQZ*1000,itemName="Dropoff QZ")
    
    print(f'{pX}\n{pY}\n{pZ}\n{pQW}\n{pQX}\n{pQY}\n{pQZ}')
    

def mainloop():
    step(stepMessage="Waiting for scan step...")
            
    root = Path(__file__).parent.absolute()
    img_name = root.joinpath("capture.jpg")
    ret = takePhoto(img_name)
    if ret:
        pose = analyzeImage(img_name)
        sendToRob(pose)
        resetPins()
        mainloop()
    else:
        main()


def main():
    if Settings.initCount == 0:
        Settings.initCount = 1
        print("[PROGRAM START]")
    else:
        print("[ERROR] Sync Lost! Returning to Init Sync...")
    setBin([1,1,1,0,1,1,0,1,1,0,1,1])
    print("Waiting for Robot Ready...")
    while not GPIO.input(robReady):
        time.sleep(.05)
    step(stepMessage="Waiting for init sync...")
    resetPins()
    mainloop()
    

# Establish Inputs
stopExec = 26 # White
robReady = 19 # White
robStep = 13 # White

# Establish Outputs
Bi1 = 21 # Blue
Bi2 = 20 # Blue
Bi3 = 16 # Blue
Bi4 = 12 # Blue
Bi5 = 1 # Yellow
Bi6 = 7 # Yellow
Bi7 = 8 # Yellow
Bi8 = 25 # Yellow
Bi9 = 24 # Green
Bi10 = 23 # Green
Bi11 = 18 # Green
BiS = 4 # Green
CamStep = 17 # Red

# Disable Pin Warnings
GPIO.setwarnings(False)

# Setup PinMode to BCM
GPIO.setmode(GPIO.BCM)

# Setup Output Pins
GPIO.setup(Bi1, GPIO.OUT)
GPIO.setup(Bi2, GPIO.OUT)
GPIO.setup(Bi3, GPIO.OUT)
GPIO.setup(Bi4, GPIO.OUT)
GPIO.setup(Bi5, GPIO.OUT)
GPIO.setup(Bi6, GPIO.OUT)
GPIO.setup(Bi7, GPIO.OUT)
GPIO.setup(Bi8, GPIO.OUT)
GPIO.setup(Bi9, GPIO.OUT)
GPIO.setup(Bi10, GPIO.OUT)
GPIO.setup(Bi11, GPIO.OUT)
GPIO.setup(BiS, GPIO.OUT)
GPIO.setup(CamStep, GPIO.OUT)

# Setup Input Pins
GPIO.setup(stopExec, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(robReady, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(robStep, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


if __name__ == "__main__":
    main()
