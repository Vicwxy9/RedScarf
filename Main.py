from ultralytics import YOLO
import cv2
import time
cap=cv2.VideoCapture(0)
MODEL_NAME="best"
model = YOLO(f'data/{MODEL_NAME}.onnx')
while True:
    now=time.time()
    ret,frame=cap.read()
    redscarfs = model(frame,conf=0.7,show=True)
    for redscarf in redscarfs:
        name = redscarf.boxes.xyxyn
        print(name)
    last=time.time()
    fps = 1/(last-now)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break