import cv2
from cvzone.HandTrackingModule import HandDetector
import pyfirmata

wCam, hCam = 640, 480

vidCap = cv2.VideoCapture(1)
vidCap.set(3, wCam)
vidCap.set(4, hCam)

detector = HandDetector(detectionCon=0.7)

if not vidCap.isOpened():
    print("Camera Tidak bisa diakses")
    exit()

pinR, pinY, pinG, pinB, pinW = 2, 3, 4, 5, 6
port = 'COM3'
board = pyfirmata.Arduino(port)

while vidCap.isOpened:
    success, img = vidCap.read()
    img = detector.findHands(img, draw=False)
    lmlist, bbox = detector.findPosition(img, draw=False)

    if lmlist:
        fingers = detector.fingersUp()
        thumb, index, middle, ring, pinky = fingers[0], fingers[1], fingers[2], fingers[3], fingers[4]
        thumbX, thumbY = lmlist[4][0], lmlist[4][1]
        indexX, indexY = lmlist[8][0], lmlist[8][1]
        middleX, middleY = lmlist[12][0], lmlist[12][1]
        ringX, ringY = lmlist[16][0], lmlist[16][1]
        pinkyX, pinkyY = lmlist[20][0], lmlist[20][1]


        if thumb == 1:
            cv2.circle(img, (thumbX, thumbY), 17, (0, 0, 255), cv2.FILLED)
        if index == 1:
            cv2.circle(img, (indexX, indexY), 17, (0, 255, 255), cv2.FILLED)
        if middle == 1:
            cv2.circle(img, (middleX, middleY), 17, (0, 255, 0), cv2.FILLED)
        if ring == 1:
            cv2.circle(img, (ringX, ringY), 17, (255, 0, 0), cv2.FILLED)
        if pinky == 1:
            cv2.circle(img, (pinkyX, pinkyY), 17, (255, 255, 255), cv2.FILLED)

        totalFingers = fingers.count(1)
        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (57, 375), cv2.FONT_ITALIC, 4, (0, 0, 0), 15)

        #print(fingers)

        MetalFinger = [thumb, index, middle, ring, pinky]
        board.digital[pinR].write(thumb)
        board.digital[pinY].write(index)
        board.digital[pinG].write(middle)
        board.digital[pinB].write(ring)
        board.digital[pinW].write(pinky)

        cv2.putText(img, 'Created by : ArduComp', (10, 450), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)
        cv2.putText(img, 'Dated : 07/12/2021', (10, 475), cv2.FONT_ITALIC, 0.7, (0, 255, 255), 2)


    cv2.imshow("image", img)
    cv2.waitKey(1)

