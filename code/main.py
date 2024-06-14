#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
from keras.models import load_model
import cv2
import numpy as np
from picamera2 import Picamera2
from time import sleep

# Thresholds and init for motion
pixel_threshold = 35
motion_threshold = 10000
previous_green = None

# Set the pin number where your servo is connected. One for dog(18) one for cat(17)
servo_pin1 = 18
servo_pin2 = 17

def prediction(im):
    im = cv2.resize(im, (224, 224), interpolation=cv2.INTER_AREA)
    im = np.asarray(im, dtype=np.float32)
    im = (im / 127.5) - 1
    im = im.reshape(1, 224, 224, 3) 
    # Predict using the model
    prediction = model.predict(im)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    # Print prediction and confidence score
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
    if(index == 0):
        return("cat")
    elif(index == 1):
        return("dog")
    else:
        return("backround")

def servo(pred):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin1, GPIO.OUT)
    GPIO.setup(servo_pin2, GPIO.OUT)
    pwm1 = GPIO.PWM(servo_pin1, 50)
    pwm2 = GPIO.PWM(servo_pin2, 50)
    def angle_to_duty_cycle(angle):
        return (0.05 * angle) + 2.5
    try:
        if(pred == "cat"):
            pwm2.start(angle_to_duty_cycle(80))
            time.sleep(3)
        if(pred == "dog"):
            pwm1.start(angle_to_duty_cycle(80))
            time.sleep(3)

    except KeyboardInterrupt:
        print("Exiting")

    finally:
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()

# Load the model and labels
timenow=time.time()
model = load_model("./models/cats_dogs/keras_model.h5", compile=False)
class_names = open("./models/cats_dogs/labels.txt", "r").readlines()

# Initialize picamera2
picam2 = Picamera2()
picam2.start()
print("starting Motion Detection")

while True:
    im = picam2.capture_array()

    if im.shape == (480, 640, 4):

        im = im[:, :, :3]
        # store green channel for motion detection
        current_green = im[:, :, 1]

        if previous_green is not None:
            
            current_green = current_green.astype(np.int16)
            # previous_green = previous_green.astype(np.int16)
            difference = np.abs(current_green - previous_green)
            significant_changes = difference > pixel_threshold
            motion_sum = np.sum(significant_changes)

            if motion_sum > motion_threshold:
                print("Motion detected!")
                if(prediction(im)=="cat"):
                    servo("cat")
                elif(prediction(im)=="dog"):
                    servo("dog")

        previous_green = current_green.copy()
