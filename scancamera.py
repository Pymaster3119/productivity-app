import cv2
import numpy as np
import urllib.request
import os
import menubar
import sounds
import time
from config import config

def download_yolo_model():
    model_files = {
        'yolov4-tiny.weights': 'https://github.com/AlexeyAB/darknet/releases/download/yolov4/yolov4-tiny.weights',
        'yolov4-tiny.cfg': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny.cfg',
        'coco.names': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names'
    }
    
    for filename, url in model_files.items():
        if not os.path.exists(filename):
            print(f"Downloading {filename}")
            urllib.request.urlretrieve(url, filename)
    return True

def load_yolo_model():
    if not download_yolo_model():
        return None, None
        
    # Load YOLO
    net = cv2.dnn.readNet('yolov4-tiny.weights', 'yolov4-tiny.cfg')
    
    # Load classes
    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
        
    return net, classes

def ai_detect_objects(frame, net, classes):
    if net is None:
        return None

    # Input preprocessing
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, config.scale_factor, (config.input_width, config.input_height), swapRB=True, crop=False)
    net.setInput(blob)
    
    # Get outputs
    layer_names = net.getLayerNames()
    unconnected = net.getUnconnectedOutLayers()
    
    output_layers = [layer_names[i - 1] for i in unconnected]
    outputs = net.forward(output_layers)
    
    # Process outputs
    boxes = []
    confidences = []
    class_ids = []
    
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            # Skip if confidence is below threshold or contains invalid values
            if confidence > config.confidence_threshold and np.isfinite(confidence):
                # Check for valid detection values
                if not (np.isfinite(detection[0]) and np.isfinite(detection[1]) and 
                       np.isfinite(detection[2]) and np.isfinite(detection[3])):
                    continue
                    
                center_x = detection[0] * width
                center_y = detection[1] * height
                w = detection[2] * width
                h = detection[3] * height
                
                # Additional safety checks
                if not (np.isfinite(center_x) and np.isfinite(center_y) and 
                       np.isfinite(w) and np.isfinite(h)):
                    continue
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([int(x), int(y), int(w), int(h)])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply non-max suppression
    if len(boxes) > 0:
        indices = cv2.dnn.NMSBoxes(boxes, confidences, config.nms_confidence_threshold, config.nms_iou_threshold)
        if len(indices) == 0:
            indices = []
    else:
        indices = []
    
    return boxes, confidences, class_ids, indices, classes

def grab_frame():
    cap = cv2.VideoCapture(0)
    print("Here")
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return None

    ret, frame = cap.read()
    cap.release()
    print("Here")

    if not ret:
        return None

    return frame

cap = cv2.VideoCapture(0)

# Load YOLO model
yolo_net, class_names = load_yolo_model()

def wait_until_human(cap):
    # Wait until there is no person (class_id == 0) in the frame
    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            time.sleep(0.1)
            continue

        detection = ai_detect_objects(frame, yolo_net, class_names)
        if detection is None:
            print("Case 1")
            return  # no detections, so assume no human

        boxes, confidences, class_ids, indices, classes = detection

        # Check if any detected object is a person (class_id == 0)
        human_present = False
        for i in indices:
            if class_ids[i] == 0:
                human_present = True
                break

        # If no human detected, break out
        if not human_present:
            print("Case 2")
            return

        time.sleep(0.1)


while True:
    ret, frame = cap.read()
    if frame is not None:
        try:
            # Detect objects using YOLO
            detection_result = ai_detect_objects(frame, yolo_net, class_names)
            if detection_result is not None:
                boxes, confidences, class_ids, indices, classes = detection_result
                segmented_frame = frame.copy()
                
                print(f"Detected {len(indices) if len(indices) > 0 else 0} objects")
                for index in range(len(indices)):
                    print(f"Object {index}: Class ID = {class_ids[indices[index]]}, Class Name = {classes[class_ids[indices[index]]]}, Confidence = {confidences[indices[index]]:.2f}")
                    if class_ids[indices[index]] == 0:
                        print("Detected a person!")
                        cap.release()
                        menubar.start_focus_timer(duration_minutes=config.camera_trigger_duration_minutes, update_interval=config.camera_trigger_update_interval, callback=sounds.start_sound)
                        cap = cv2.VideoCapture(0)
                        wait_until_human(cap)
                        sounds.stop_sound()
                print("-"*30)
        except Exception as e:
            print(f"Error in object detection: {e}")
            time.sleep(0.1)  # Small delay to prevent rapid error loops