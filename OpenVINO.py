from pathlib import Path
import cv2
from typing import Tuple
from ultralytics.yolo.utils import ops
import torch
import numpy as np
from typing import Tuple, Dict
from openvino.runtime import Core, Model
from ultralytics.yolo.utils.plotting import colors

def plot_one_box(box:np.ndarray, img:np.ndarray, color:Tuple[int, int, int] = None, mask:np.ndarray = None, label:str = None, line_thickness:int = 5):
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1 
    color = color
    c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    
    blk = np.zeros(img.shape, np.uint8)  
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    cv2.rectangle(blk, c1, c2, (255, 0, 0), -1)
    img = cv2.addWeighted(img, 1.0, blk, 0.25, 1)
    
    if label:
        tf = max(tl - 1, 1)
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + int(box[2]) - int(box[0]), c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
    return img

def draw_results(results:Dict, source_image:np.ndarray):
    boxes = results["det"]
    h, w = source_image.shape[:2]
    for idx, (*xyxy, conf, lbl) in enumerate(boxes):
        if conf >= 0.7:
            label = f'redscarf {conf:.2f}'
            source_image = plot_one_box(xyxy, source_image, label=label, color=colors(int(lbl)), line_thickness=1)
    return source_image

def letterbox(img: np.ndarray, new_shape:Tuple[int, int] = (640, 640), color:Tuple[int, int, int] = (114, 114, 114), auto:bool = False, scale_fill:bool = False, scaleup:bool = False, stride:int = 32):
    shape = img.shape[:2]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:
        r = min(r, 1.0)
    ratio = r, r 
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    if auto: 
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)
    elif scale_fill:
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0] 

    dw /= 2 
    dh /= 2

    if shape[::-1] != new_unpad: 
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
    return img, ratio, (dw, dh)

def preprocess_image(img0: np.ndarray):
    img = letterbox(img0)[0]

    img = img.transpose(2, 0, 1)
    img = np.ascontiguousarray(img)
    return img

def image_to_tensor(image:np.ndarray):
    input_tensor = image.astype(np.float32) 
    input_tensor /= 255.0 

    if input_tensor.ndim == 3:
        input_tensor = np.expand_dims(input_tensor, 0)
    return input_tensor

def postprocess(
    pred_boxes:np.ndarray,
    input_hw:Tuple[int, int],
    orig_img:np.ndarray,
    min_conf_threshold:float = 0.25,
    nms_iou_threshold:float = 0.7,
    agnosting_nms:bool = False,
    max_detections:int = 300,
    pred_masks:np.ndarray = None,
    retina_mask:bool = False
):
    nms_kwargs = {"agnostic": agnosting_nms, "max_det":max_detections}
    preds = ops.non_max_suppression(
        torch.from_numpy(pred_boxes),
        min_conf_threshold,
        nms_iou_threshold,
        nc=1,
        **nms_kwargs
    )
    results = []
    proto = torch.from_numpy(pred_masks) if pred_masks is not None else None

    for i, pred in enumerate(preds):
        shape = orig_img[i].shape if isinstance(orig_img, list) else orig_img.shape
        if not len(pred):
            results.append({"det": [], "segment": []})
            continue
        if proto is None:
            pred[:, :4] = ops.scale_boxes(input_hw, pred[:, :4], shape).round()
            results.append({"det": pred})
            continue
        if retina_mask:
            pred[:, :4] = ops.scale_boxes(input_hw, pred[:, :4], shape).round()
            masks = ops.process_mask_native(proto[i], pred[:, 6:], pred[:, :4], shape[:2])  # HWC
            segments = [ops.scale_segments(input_hw, x, shape, normalize=False) for x in ops.masks2segments(masks)]
        else:
            masks = ops.process_mask(proto[i], pred[:, 6:], pred[:, :4], input_hw, upsample=True)
            pred[:, :4] = ops.scale_boxes(input_hw, pred[:, :4], shape).round()
            segments = [ops.scale_segments(input_hw, x, shape, normalize=False) for x in ops.masks2segments(masks)]
        results.append({"det": pred[:, :6].numpy(), "segment": segments})
    return results

def detect(image:np.ndarray, model:Model):
    num_outputs = len(model.outputs)
    preprocessed_image = preprocess_image(image)
    input_tensor = image_to_tensor(preprocessed_image)
    result = model(input_tensor)
    boxes = result[model.output(0)]
    masks = None
    if num_outputs > 1:
        masks = result[model.output(1)]
    input_hw = input_tensor.shape[2:]
    detections = postprocess(pred_boxes=boxes, input_hw=input_hw, orig_img=image, pred_masks=masks)
    return detections

DET_MODEL_NAME = "/best"
det_model_path = Path(f"./{DET_MODEL_NAME}_openvino_model/{DET_MODEL_NAME}.xml")
core = Core()
det_ov_model = core.read_model(det_model_path)
device = "CPU" 
det_compiled_model = core.compile_model(det_ov_model, device)

import time
cap=cv2.VideoCapture(0)

while True:
    time1 = time.time()
    ret,frame=cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    detections = detect(frame, det_compiled_model)[0]
    image_with_boxes = cv2.cvtColor(draw_results(detections, frame), cv2.COLOR_BGR2RGB)
    time2 = time.time()
    cv2.putText(image_with_boxes, str(round(1/(time2-time1),2)), (50,50), 0, 1, [225, 255, 255], thickness=1, lineType=cv2.LINE_AA)
    cv2.imshow("res",image_with_boxes)
    
    key = cv2.waitKey(1)
    if key == 27:
        break