from pathlib import Path
from ultralytics import YOLO
det_model = YOLO('yolov8n.pt')
DET_MODEL_NAME = "yolov8n"
det_model_path = Path(f"./{DET_MODEL_NAME}_openvino_model/{DET_MODEL_NAME}.xml")
if not det_model_path.exists():
    det_model.export(format="openvino", dynamic=True, half=False)