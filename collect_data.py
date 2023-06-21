import math
import os
import time
import cv2
from string import ascii_letters

from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

OFFSET = 20
IMGSIZE = 300
FOLDER = "Data/"

char_counter = {}

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand["bbox"]

        imgWhite = np.ones((IMGSIZE, IMGSIZE, 3), np.uint8) * 255
        imgCrop = img[y - OFFSET : y + h + OFFSET, x - OFFSET : x + w + OFFSET]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        try:
            if aspectRatio > 1:
                k = IMGSIZE / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, IMGSIZE))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((IMGSIZE - wCal) / 2)
                imgWhite[:, wGap : wCal + wGap] = imgResize

            else:
                k = IMGSIZE / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (IMGSIZE, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((IMGSIZE - hCal) / 2)
                imgWhite[hGap : hCal + hGap, :] = imgResize
        except:
            continue

        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == -1:
        continue
    char = chr(key)
    if char in ascii_letters:
        char = char.upper()
        char_counter.setdefault(char, 0)
        char_counter[char] += 1
        sample_folder = f"{FOLDER}{char}"
        if not os.path.exists(sample_folder):
            os.makedirs(sample_folder)
        cv2.imwrite(f"{sample_folder}/Image_{time.time()}.jpg", imgWhite)
        print(f"{char} - {char_counter[char]}")
