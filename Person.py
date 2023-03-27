import cv2

import time
from cvzone.PoseModule import PoseDetector
detector = PoseDetector()
cap=cv2.VideoCapture(0)
while True:
    time1 = time.time()
    ret,frame=cap.read()
    img=detector.findPose(img=frame)
    list,bbox=detector.findPosition(img)
    time2 = time.time()
    print(round(1/(time2-time1),2))
    cv2.imshow("MYResult",img)
    cv2.waitKey(1)