import math

import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

OFFSET = 20
IMGSIZE = 300

with open("Model/labels.txt", "r") as f:
    content = f.read().strip().split("\n")
    labels = [v.split(" ")[1] for v in content]

while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((IMGSIZE, IMGSIZE, 3), np.uint8) * 255
        imgCrop = img[y - OFFSET:y + h + OFFSET, x - OFFSET:x + w + OFFSET]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        try:
            if aspectRatio > 1:
                k = IMGSIZE / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, IMGSIZE))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((IMGSIZE - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
                print(prediction, index)

            else:
                k = IMGSIZE / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (IMGSIZE, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((IMGSIZE - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
                prediction, index = classifier.getPrediction(imgWhite, draw=False)
        except:
            continue

        cv2.rectangle(imgOutput, (x - OFFSET, y - OFFSET-50),
                      (x - OFFSET+90, y - OFFSET-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-OFFSET, y-OFFSET),
                      (x + w+OFFSET, y + h+OFFSET), (255, 0, 255), 4)

    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)
