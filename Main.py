from detector.persondetector import PersonDetector
from detector.redscarfdetector import RedScarfDetector
from Log import log
from pathlib import Path
from openvino.runtime import Core

import cv2
import time

PERSON_MODEL_NAME = "yolov8n"
REDSCARF_MODEL_NAME = "redscarf"
DEVICE = "CPU" 

log("Program start (by Vicwxy Wangxinyu).")

core = Core()
log("OpenVINO core load complete.")

person_model_path = Path(f"./models/{PERSON_MODEL_NAME}_openvino_model/{PERSON_MODEL_NAME}.xml")
person_ov_model = core.read_model(person_model_path)
person_compiled_model = core.compile_model(person_ov_model, DEVICE)
log("The model for person load complete.")

redscarf_model_path = Path(f"./models/{REDSCARF_MODEL_NAME}_openvino_model/{REDSCARF_MODEL_NAME}.xml")
redscarf_ov_model = core.read_model(redscarf_model_path)
redscarf_compiled_model = core.compile_model(redscarf_ov_model, DEVICE)
log("The model for redscarf load complete.")

log("Loading camera 0 (If you want to change the camera , please change the codes).")
cap=cv2.VideoCapture(0)
log("Loading complete. Initiation recognition.....")

while True:
    start_time = time.time()
    
    _, frame=cap.read()
    RedScarfs = []
    res, RedScarfs = RedScarfDetector(frame, frame, redscarf_compiled_model)
    res            = PersonDetector(  res,   frame, person_compiled_model, redscrafs=RedScarfs)
    
    fps = 1 / (time.time() - start_time)
    fps_text = f"FPS: {fps:.2f}"
    color = (0,0,0)
    cv2.putText(res, fps_text, (int(res.shape[1]/2)-int((len(fps_text))*9), 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
    cv2.imshow("Demo", res)
    
    if cv2.waitKey(1) == 27:
        break
