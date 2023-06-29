#!/usr/bin python generate_aruco.py
"""generate_aruco.py: Generates aruco tags to be used by robot vision and OpenCV for 3D locating information.
"""

__version__ = "1.0.0"

__author__ = "Matthew DiMaggio"
__date__ = "14 June 2023"

import numpy as np
import cv2
from cv2 import aruco

def generateTag(tag_id, tag_type, tag_size):

    output = f'tag/{tag_type}_id{tag_id}.png'

    arucoDict = aruco.getPredefinedDictionary(eval(f'aruco.{tag_type}'))

    print(f'[INFO] Generating ArUCo tag type {tag_type} with ID {tag_id}')

    img = np.zeros((tag_size, tag_size, 1), dtype=np.uint8)

    aruco.generateImageMarker(arucoDict, tag_id, tag_size, img, 1)

    cv2.imwrite(output, img)


for i in range(100):
    generateTag(i, "DICT_5X5_100", 300)