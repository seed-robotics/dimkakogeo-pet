#!/usr/bin/python3

from keras.models import load_model
import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
from time import sleep


# Thresholds and init
pixel_threshold = 35
motion_threshold = 10000
previous_green = None
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
print("starting Motion Detection")
while True:
    im = picam2.capture_array()
    # print(im)
    # print(im.shape)
    if im.shape == (480, 640, 4):
        # Extract the RGB channels and ignore the alpha channel
        im = im[:, :, :3]
        green = im[:, :, 1]

        current_green = im[:, :, 1]
        # print(previous_green)
        if previous_green is not None:
            current_green = current_green.astype(np.int16)
            previous_green = previous_green.astype(np.int16)
            #abs = absolut 
            difference = np.abs(current_green - previous_green)
            significant_changes = difference > pixel_threshold
            motion_sum = np.sum(significant_changes)
            print("sum:", motion_sum)

            if motion_sum > motion_threshold:
                print(significant_changes)
                print("Motion detected!")

        previous_green = current_green.copy()
