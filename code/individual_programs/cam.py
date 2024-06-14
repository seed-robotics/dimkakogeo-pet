#!/usr/bin/python3
from keras.models import load_model
import cv2
import numpy as np
from picamera2 import Picamera2
from libcamera import controls
from time import sleep

# Load the model and labels
model = load_model("./models/cats_dogs/keras_model.h5", compile=False)
class_names = open("./models/cats_dogs/labels.txt", "r").readlines()

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})

while True:
    im = picam2.capture_array()

    if im.shape == (480, 640, 4):
        # Extract the RGB channels and ignore the alpha channel
        im = im[:, :, :3]

        im = cv2.resize(im, (224, 224), interpolation=cv2.INTER_AREA)
        # #cv2.imshow("Webcam Image", im)


        im = np.asarray(im, dtype=np.float32)
        im = (im / 127.5) - 1
        im = im.reshape(1, 224, 224, 3)

        # # Predict using the model
        prediction = model.predict(im)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]
        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        print("Print class:", class_name)
        

# Release resources
picam2.stop()
cv2.destroyAllWindows()

